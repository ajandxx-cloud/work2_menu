from math import exp
from numpy.random import gumbel
import numpy as np
from Environments.OOH.containers import ChoiceResult, MenuOffer

class customerchoicemodel(object):
    def __init__(self,
                 base_util,
                 dist_scaler,
                 euclidean,
                 dist_mat,
                 n_cust,
                 outside_option_util=0.0,
                 service_mode="mixed"):
        self.euclidean_distance = euclidean
        self.dist_scaler = dist_scaler
        self.base_util = base_util
        self.dist_mat = dist_mat
        self.n_cust = n_cust
        self.outside_option_util = outside_option_util
        self.service_mode = service_mode
        if len(self.dist_mat)>0:
            self.mnl = self.mnl_distmat
        else:
            self.mnl = self.mnl_euclid

    def _outside_enabled(self):
        return self.outside_option_util is not None

    def _argmax_with_optional_outside(self, service_utils):
        utilities = []
        if self._outside_enabled():
            utilities.append(float(self.outside_option_util))
        utilities.extend([float(value) for value in service_utils])
        noisy = np.asarray(utilities, dtype=float).reshape((-1, 1))
        noisy = np.add(noisy, gumbel(0, 1, np.shape(noisy)))
        idx = int(np.argmax(noisy))
        if self._outside_enabled() and idx == 0:
            return None
        return idx - 1 if self._outside_enabled() else idx
        
    def mnl_euclid(self,customer,parcelpoint):
        """
        multi-nomial logit model calculating euclidean distance
        """
        distance = self.euclidean_distance(customer.home,parcelpoint.location)#distance from parcelpoint to home
        beta_p = -exp(-distance/self.dist_scaler)
        return self.base_util + beta_p

    def mnl_distmat(self,customer,parcelpoint):
        """
        multi-nomial logit model using distance matrix
        """
        distance = self.dist_mat[customer.id_num][parcelpoint.id_num]#distance from parcelpoint to home
        beta_p = -exp(-distance/self.dist_scaler)
        return self.base_util + beta_p
    
    def customerchoice_offer(self,customer,action,parcelpoints):
        """
        Customer choice model for the offering decision, i.e., action is 1 parcelpoint offer
        """
        if self.service_mode == "home_only":
            chosen = self._argmax_with_optional_outside([self.base_util + customer.home_util])
            if chosen is None:
                return ChoiceResult.opted_out({"reason": "outside_option"})
            return customer.home, False, -1, 0
        pps = parcelpoints[action-self.n_cust]
        if len(pps) == 0:
            if self.service_mode == "ooh_only":
                return ChoiceResult.opted_out({"reason": "empty_ooh_menu"})
            chosen = self._argmax_with_optional_outside([self.base_util + customer.home_util])
            if chosen is None:
                return ChoiceResult.opted_out({"reason": "outside_option"})
            return customer.home, False, -1, 0
        if self.service_mode == "ooh_only":
            utils = []
            for idx, pp in enumerate(pps):
                utils.append(self.mnl(customer, pp))
            idx = self._argmax_with_optional_outside(utils)
            if idx is None:
                return ChoiceResult.opted_out({"reason": "outside_option"})
            return pps[idx].location, True, pps[idx].id_num, 0
        utils = [self.base_util + customer.home_util]
        for idx,pp in enumerate(pps):
            utils.append(self.mnl(customer,pp))

        idx = self._argmax_with_optional_outside(utils)
        if idx is None:
            return ChoiceResult.opted_out({"reason": "outside_option"})
        if idx==0:
            return customer.home, False, -1, 0#home delivery
        else:
            return pps[idx-1].location, True, pps[idx-1].id_num,0#accept offer

    def customerchoice_pricing(self,customer,action,parcelpoints):
        """
        Customer choice model for the pricing decision, i.e., action is vector of prices for all PPs and home delivery
        """
        if self.service_mode == "home_only":
            home_util = self.base_util + customer.home_util + customer.incentiveSensitivity * float(action[0])
            chosen = self._argmax_with_optional_outside([home_util])
            if chosen is None:
                return ChoiceResult.opted_out({"reason": "outside_option"})
            return customer.home, False, -1, action[0]
        pps = parcelpoints[parcelpoints.mask].data
        if len(pps) == 0:
            if self.service_mode == "ooh_only":
                return ChoiceResult.opted_out({"reason": "empty_ooh_menu"})
            home_util = self.base_util + customer.home_util + customer.incentiveSensitivity * float(action[0])
            chosen = self._argmax_with_optional_outside([home_util])
            if chosen is None:
                return ChoiceResult.opted_out({"reason": "outside_option"})
            return customer.home, False, -1, action[0]
        if self.service_mode == "ooh_only":
            utils = []
            for idx, pp in enumerate(pps):
                utils.append(self.mnl(customer, pp) + customer.incentiveSensitivity * float(action[idx + 1]))
            idx = self._argmax_with_optional_outside(utils)
            if idx is None:
                return ChoiceResult.opted_out({"reason": "outside_option"})
            return pps[idx].location, True, pps[idx].id_num, action[idx + 1]
        utils = [self.base_util + customer.home_util]
        for idx,pp in enumerate(pps):
            utils.append(self.mnl(customer,pp))
        utils = [utility + customer.incentiveSensitivity * float(price)
                 for utility, price in zip(utils, action)]
        idx = self._argmax_with_optional_outside(utils)
        if idx is None:
            return ChoiceResult.opted_out({"reason": "outside_option"})
        if idx==0:
            return customer.home, False, -1, action[0]#home delivery
        else:
            return pps[idx-1].location, True, pps[idx-1].id_num,action[idx]#accept offer

    def customerchoice_menu(self, customer, offers):
        """MNL choice over displayed MenuOffer objects plus outside option."""
        if self.service_mode == "home_only":
            offers = [offer for offer in offers if offer.is_home]
        elif self.service_mode == "ooh_only":
            offers = [offer for offer in offers if not offer.is_home]
        if len(offers) == 0:
            return ChoiceResult.opted_out({"reason": "empty_menu"})

        utilities = []
        include_outside = self.outside_option_util is not None
        if include_outside:
            utilities.append(float(self.outside_option_util))
        for offer in offers:
            if not isinstance(offer, MenuOffer):
                raise TypeError("customerchoice_menu expects MenuOffer actions")
            if offer.predicted_utility is not None:
                utility = float(offer.predicted_utility)
            else:
                base = self.base_util + (customer.home_util if offer.is_home else 0.0)
                if offer.is_home:
                    distance_term = 0.0
                else:
                    distance = self.euclidean_distance(customer.home, offer.location)
                    distance_term = -exp(-distance / max(self.dist_scaler, 1.0))
                utility = base + distance_term + customer.incentiveSensitivity * float(offer.price)
            utilities.append(utility)

        noisy = np.asarray(utilities, dtype=float).reshape((-1, 1))
        noisy = np.add(noisy, gumbel(0, 1, np.shape(noisy)))
        idx = int(np.argmax(noisy))
        if include_outside and idx == 0:
            return ChoiceResult.opted_out({
                "reason": "outside_option",
                "displayed_menu_size": int(len(offers)),
            })

        offer = offers[idx - 1] if include_outside else offers[idx]
        if offer.is_home:
            return ChoiceResult.accepted_home(
                offer.location,
                offer=offer,
                price=offer.price,
                metadata={"displayed_menu_size": int(len(offers))},
            )
        return ChoiceResult.accepted_meeting_point(
            offer.location,
            offer.parcelpoint_id,
            offer=offer,
            price=offer.price,
            metadata={"displayed_menu_size": int(len(offers))},
        )

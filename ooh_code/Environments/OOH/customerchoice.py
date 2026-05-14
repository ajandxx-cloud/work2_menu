from math import exp
from typing import Iterable, List

import numpy as np

from Environments.OOH.containers import MenuOffer


class customerchoicemodel:
    def __init__(self, base_util, dist_scaler, travel_time_weight=0.0, pickup_time_weight=0.0, outside_option_util=0.0):
        self.dist_scaler = dist_scaler
        self.base_util = base_util
        self.travel_time_weight = travel_time_weight
        self.pickup_time_weight = pickup_time_weight
        self.outside_option_util = outside_option_util
        self.rng = np.random.RandomState()
        self.opt_out_count = 0

    def set_rng(self, rng):
        self.rng = rng if rng is not None else np.random.RandomState()

    def _menu_offer_utility(self, customer, offer: MenuOffer) -> float:
        if offer.is_home:
            base = self.base_util + customer.home_util
        else:
            base = self.base_util
        return (
            base
            + customer.incentiveSensitivity * float(offer.price)
            + self.travel_time_weight * float(offer.predicted_in_vehicle_time)
            + self.pickup_time_weight * float(offer.time_deviation)
            - (1.0 - exp(-float(offer.walk_distance) / max(self.dist_scaler, 1.0)))
        )

    def customerchoice_menu(self, customer, action: Iterable[MenuOffer], _meeting_points):
        offers: List[MenuOffer] = list(action)
        if len(offers) == 0:
            return customer.home, False, -1, 0.0, None

        n_offers = len(offers)
        utils = np.empty((n_offers + 1, 1))
        for idx, offer in enumerate(offers):
            utility = self._menu_offer_utility(customer, offer)
            offer.predicted_utility = float(utility)
            utils[idx] = utility
        utils[n_offers] = self.outside_option_util

        utils = np.add(utils, self.rng.gumbel(0, 1, np.shape(utils)))
        idx = int(np.argmax(utils))

        if idx == n_offers:  # outside option chosen — passenger opts out
            self.opt_out_count += 1
            # Fall back to home offer so last_selected_offer is non-None for model update().
            # Tag the home offer metadata so _log_menu_decision can set opted_out=True.
            home_offer = next((o for o in offers if o.is_home), None)
            if home_offer is not None:
                if home_offer.metadata is None:
                    home_offer.metadata = {}
                home_offer.metadata["opted_out"] = True
            return customer.home, False, -1, 0.0, home_offer

        chosen_offer = offers[idx]
        if chosen_offer.is_home:
            return customer.home, False, -1, float(chosen_offer.price), chosen_offer
        return chosen_offer.location, True, chosen_offer.parcelpoint_id, float(chosen_offer.price), chosen_offer

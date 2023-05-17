from os import write
from nyct_gtfs import NYCTFeed
from datetime import datetime

class Stations:
    N_4_AV_9ST = "F23N"
    N_7_AV = "F24N"
    S_4_AV_9ST = "F23S"
    S_7_AV = "F24S"

class StationArrivals:
    @staticmethod
    def __unique_route_id_feeds(route_ids):
        route_id_2_url_dict = NYCTFeed._train_to_url
        url_2_route_id = {
            feed: route_id
            for route_id, feed in route_id_2_url_dict.items()
        }
        feeds = set(map(route_id_2_url_dict.get, route_ids))
        return [url_2_route_id[feed] for feed in feeds]

    def __init__(self, api_key, route_ids, station_ids):
        print(api_key, route_ids, station_ids)
        unique_route_ids_for_feeds = self.__unique_route_id_feeds(route_ids)
        print(unique_route_ids_for_feeds)
        self.__route_ids = route_ids
        self.__station_ids = station_ids
        self.__train_feeds = [NYCTFeed(route_id, api_key=api_key) for route_id in unique_route_ids_for_feeds]
        self.__arrival_trains = []

    def directional_arrival(self, directions, length=5):
        if not self.__arrival_trains:
            self.refresh()
        arrival_trains = self.__arrival_trains
        return [*filter(
                    lambda train: train.direction in set(directions),
                    arrival_trains)][:length]

    def refresh(self):
        for train_feed in self.__train_feeds:
            train_feed.refresh()
        self.__arrival_trains = self.__get_station_arrivals()

    def __get_trains(self):
        route_ids = self.__route_ids
        station_ids = self.__station_ids
        train_feeds = self.__train_feeds
        routes = map(lambda f: f.filter_trips(route_ids, headed_for_stop_id=station_ids),
                    train_feeds)
        return [train   for trains_in_route in routes
                        for train in trains_in_route]

    def __get_arrival_time_for_train(self, train):
        station_ids = self.__station_ids
        for stop_time_update in train.stop_time_updates:
            if stop_time_update.stop_id in station_ids:
                return stop_time_update.arrival
        raise Exception("Data corrupted");

    def __get_station_arrivals(self):
        trains = self.__get_trains()
        return sorted(trains, key=self.__get_arrival_time_for_train)

    def format(self, trains):
        def format_train(train):
            arrival_time = self.__get_arrival_time_for_train(train)
            arrival_delta_in_secs = int((arrival_time - datetime.now()).total_seconds())
            arrival_delta_in_mins = int(arrival_delta_in_secs//60)
            return {
                "route_id": train.route_id,
                "arrival_time": arrival_time.isoformat(),
                "arrival_delta_in_mins": arrival_delta_in_mins,
                "arrival_delta_in_secs": arrival_delta_in_secs,
                "direction": train.direction,
                "trip_id": train.trip_id,
                "destination": train.headsign_text,
                "extra": str(train)
            }
        return [format_train(t) for t in trains]


    def debug(self, trains):
        def debug_train(train):
            arrival_time = self.__get_arrival_time_for_train(train)
            arrival_delta_mins = int((arrival_time - datetime.now()).total_seconds()//60)
            print("\t".join([
                f"{train.route_id} ┊".rjust(4),
                f"{arrival_delta_mins} mins ┊".rjust(10),
                f"{train.direction} ┊".rjust(4),
                f"{str(train)}"
            ]))
        for train in trains:
            debug_train(train)

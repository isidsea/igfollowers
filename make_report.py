from lib.reporting.cross_followers import Engine as CFEngine
from lib.engine.aggregator         import Engine as AggregatorEngine
import sys

if __name__ == "__main__":
	# For cross followers engine, we need to aggregate the user first before making a report
	# aggregator = AggregatorEngine()
	# aggregator.aggregate_user()

	cf_engine = CFEngine()
	cf_engine.generate()
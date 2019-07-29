import sys

from autoscaler.modes.abstractmode import AbstractMode
from autoscaler.modes.scalecpu import ScaleByCPU
from autoscaler.modes.scalemem import ScaleByMemory
from autoscaler.modes.scalesqs import ScaleBySQS


class ScaleByCPUMemorySQS(AbstractMode):

    def __init__(self,  api_client=None, app=None, dimension=None):
        super().__init__(api_client, app)

        # Defines the individual scaling modes
        self.mode_map = {
            'cpu': ScaleByCPU,
            'mem': ScaleByMemory,
            'sqs': ScaleBySQS
        }

        if len(dimension['min']) < 3 or len(dimension['max']) < 3:
            self.log.error("Scale mode requires three comma-delimited "
                           "values for MIN_RANGE and MAX_RANGE.")
            sys.exit(1)

        # Instantiate the mode classes with min/max
        for idx, mode in enumerate(list(self.mode_map.keys())):
            self.mode_map[mode] = self.mode_map[mode](
                api_client,
                app,
                dimension={
                    'min': dimension['min'][idx],
                    'max': dimension['max'][idx]
                }
            )

    def scale_direction(self):
        """
        Test CPU (x), Memory (y) , and SQS (z) direction for equality.
        If (x = y = z), return x, otherwise return 0.
        """
        results = []

        try:
            for mode in list(self.mode_map.keys()):
                results.append(self.mode_map[mode].scale_direction())
        except ValueError:
            raise

        self.log.info("CPU direction = %s, Memory direction = %s, SQS direction = %s",
                      results[0], results[1], results[2])

        if results[0] == results[1] == results[2]:
            return results[0]
        else:
            return 0

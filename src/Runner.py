from abc import ABC, abstractmethod
import time
from typing import List


class Runner(ABC):
    """This class defines a Runner.
    
    A Runner is a type that we use for our Benchmark, like all APIs that we test
    are implemented using a runner, the API calls are made inside of the "run" function
    """

    def write_result(self, token: List[str], amounts_in: List[int], amounts_out: List[int], duration: List[float]):
        """Write the given result inside of a file

        :param token: The address of the token that we are selling
        :type token: List[str]
        :param amounts_in: The amount of the token that we put in
        :type amounts_in: List[int]
        :param amounts_out: The amount of the token that we put out
        :type amounts_out: List[int]
        :param duration: The amount of seconds that we took to handle the token
        :type duration: float
        """

    @abstractmethod
    async def run(self):
        """Run the API calls and write the results inside of a CSV file.
        
        You implement the API call that you want to time in here.
        """

    async def time_run(self) -> float:
        """Calls the "run" method and time the amount it took to get the result

        :return: The number of seconds that the "run" method took to execute
        :rtype: float
        """
        start = time.time()
        await self.run()
        return time.time() - start

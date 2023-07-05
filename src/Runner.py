from abc import ABC, abstractmethod
import csv
from decimal import Decimal
import time
from typing import List, Tuple


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
        to_write = []
        total_amount_out = Decimal(0)
        for i in range(len(token)):
            total_amount_out += Decimal(amounts_out[i]) / Decimal(10**18)
            to_write.append([
                token[i],
                amounts_in[i],
                Decimal(amounts_out[i]) / Decimal(10**18),
                duration[i]
            ])

        to_write.append(["", "", "", ""])
        to_write.append(["", "Total Amount out:", total_amount_out])
        to_write.append(["", "Average duration:", sum(duration) / len(duration)])

        with open("dest_blockchain.csv", "w+") as f:
            writer = csv.writer(f)
            writer.writerow([
                "Token Address",
                "Amount in",
                "Amount out",
                "Duration"
            ])
            writer.writerows(to_write)
            

    @abstractmethod
    async def run(self) -> Tuple[List[str], List[int], List[int], List[float]]:
        """Run the API calls and write the results inside of a CSV file.
        
        You implement the API call that you want to time in here.
        
        :returns: A tuple containing the call parameters for write_result:
                  - At first the list containing the address of the token
                  - At second the list of amount_in
                  - At third the list of amount out
                  - At 4th the duration of the call
        :rtype: Tuple[List[str], List[int], List[int], List[float]]
        """

    async def time_run(self) -> float:
        """Calls the "run" method and time the amount it took to get the result

        :return: The number of seconds that the "run" method took to execute
        :rtype: float
        """
        start = time.time()
        result = await self.run()
        duration = time.time() - start
        self.write_result(result[0], result[1], result[2], result[3])
        return duration

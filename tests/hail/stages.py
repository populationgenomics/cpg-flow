import json

from cpg_flow.stage import SequencingGroupStage, Stage, StageInput, StageOutput, stage
from cpg_flow.targets.sequencing_group import SequencingGroup
from cpg_utils.hail_batch import get_batch

"""
Here's a fun programming task with four interdependent steps, using the concept of **prime numbers** and their relationships:

---

### Task: Prime Pyramid
Write a program that builds a "Prime Pyramid" based on a given input number \( N \). The pyramid is built in four steps:

#### Step 1: **Generate Prime Numbers**
Write a function to generate the first \( N \) prime numbers. For example, if \( N = 5 \), the output would be `[2, 3, 5, 7, 11]`.

#### Step 2: **Calculate Cumulative Sums**
Using the prime numbers generated in Step 1, calculate a list of cumulative sums. Each cumulative sum is the sum of the primes up to that index.
Example: For `[2, 3, 5, 7, 11]`, the cumulative sums are `[2, 5, 10, 17, 28]`.

#### Step 3: **Filter Even Numbers**
From the cumulative sums generated in Step 2, filter out the even numbers.
Example: For `[2, 5, 10, 17, 28]`, the result is `[5, 17]`.

#### Step 4: **Build the Prime Pyramid**
Using the filtered numbers from Step 3, construct a pyramid. Each level of the pyramid corresponds to a filtered number, and the number determines how many stars `*` appear on that level.
Example: For `[5, 17]`, the pyramid is:
```
*****
*****************
```

---

### Optional Extensions:
1. Allow the user to input \( N \) dynamically.
2. Visualize the pyramid with formatting, like centering the stars.
3. Add validation to ensure \( N \) is a positive integer.
4. Include unit tests for each step.

This task is simple, yet it combines loops, conditionals, and basic data manipulations in a creative way!
"""


@stage
class GeneratePrimes(SequencingGroupStage):
    def expected_outputs(self, sequencing_group: SequencingGroup) -> dict[str, str]:
        return {
            'id_sum': self.output_file(sequencing_group, 'primes'),
            'primes': self.output_file(sequencing_group, 'primes'),
        }

    def queue_jobs(self, sequencing_group: SequencingGroup, inputs: StageInput) -> StageOutput | None:
        # Calculate sum of sg id digits
        id_sum = self.iterative_digit_sum_from_string(sequencing_group.id)

        # Generate id_sum number of primes
        primes = self.first_n_primes(id_sum)

        # Get batch
        b = get_batch()
        j = b.new_job(name='generate-primes')

        # Write primes to output file
        j.command(f"echo '{json.dumps(primes)}' > {j.primes}")
        j.write_output(j.primes, self.expected_outputs(sequencing_group).get('primes'))

        # Write id_sum to output file
        j.command(f"echo '{id_sum}' > {j.id_sum}")
        j.write_output(j.id_sum, self.expected_outputs(sequencing_group).get('id_sum'))

        jobs = [j]

        return self.make_outputs(sequencing_group, data=self.expected_outputs(sequencing_group), jobs=jobs)

    def iterative_digit_sum_from_string(self, s):
        # Extract digits from the string
        digits = [int(char) for char in s if char.isdigit()]
        # Calculate the sum iteratively
        n = sum(digits)
        while n >= 10:
            n = sum(int(digit) for digit in str(n))
        return n

    def first_n_primes(self, n: int) -> list[int]:
        def is_prime(num):
            """Check if a number is prime."""
            if num < 2:
                return False

            return all(num % i != 0 for i in range(2, int(num**0.5) + 1))

        # Start checking from 2
        primes: list[int] = []
        candidate = 2
        while len(primes) < n:
            if is_prime(candidate):
                primes.append(candidate)
            candidate += 1

        return primes


@stage(
    requires=[GeneratePrimes],
)
class CumulativeCalc(SequencingGroupStage):
    def output_file(self, sequencing_group: SequencingGroup) -> str:
        return f'{sequencing_group.id}-cumulative.txt'

    def expected_outputs(self, sequencing_group: SequencingGroup):
        return {
            'cumulative': self.output_file(sequencing_group),
        }

    def queue_jobs(self, sequencing_group: SequencingGroup, inputs: StageInput) -> StageOutput | None:
        input_json = inputs.as_path(sequencing_group, GeneratePrimes, 'primes')
        primes = json.load(open(input_json))

        cumulative = self.cumulative_sum(primes)

        b = get_batch()
        j = b.new_job(name='cumulative-calc')

        # Write cumulative sums to output file
        j.command(f"echo '{json.dumps(cumulative)}' > {j.cumulative}")
        j.write_output(j.cumulative, self.expected_outputs(sequencing_group).get('cumulative'))

        return self.make_outputs(sequencing_group, data=self.expected_outputs(sequencing_group), jobs=[j])

    def cumulative_sum(self, primes: list[int]) -> list[int]:
        csum = 0
        cumulative = []
        for i in range(len(primes)):
            csum += primes[i]
            cumulative.append(csum)

        return cumulative


@stage(
    requires=[CumulativeCalc],
)
class FilterEvens(SequencingGroupStage):
    def expected_outputs(self, sequencing_group: SequencingGroup):
        """
        Override to declare expected output paths.
        """
        pass

    def queue_jobs(self, sequencing_group: SequencingGroup, inputs: StageInput) -> StageOutput | None:
        """
        Override to add Hail Batch jobs.
        """
        pass


@stage(
    required_stage=[GeneratePrimes, FilterEvens],
)
class BuildAPrimePyramid(SequencingGroupStage):
    def expected_outputs(self, sequencing_group: SequencingGroup):
        """
        Override to declare expected output paths.
        """
        pass

    def queue_jobs(self, sequencing_group: SequencingGroup, inputs: StageInput) -> StageOutput | None:
        """
        Override to add Hail Batch jobs.
        """
        pass

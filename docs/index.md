# Continuous Intelligence

This site provides documentation for this project.
Use the navigation to explore module-specific materials.

## How-To Guide

Many instructions are common to all our projects.

See
[⭐ **Workflow: Apply Example**](https://denisecase.github.io/pro-analytics-02/workflow-b-apply-example-project/)
to get these projects running on your machine.

## Project Documentation Pages (docs/)

- **Home** - this documentation landing page
- **Project Instructions** - instructions specific to this module
- **Your Files** - how to copy the example and create your version
- **Glossary** - project terms and concepts

## Additional Resources

- [Suggested Datasets](https://denisecase.github.io/pro-analytics-02/reference/datasets/cintel/)

## Custom Project

### Dataset
I used a data set from Kaggle.com that focused on a machine's optimal operating conditions. It focused on the machine's temperature, speed, vibration and energy usage to calculate production quality and whether or not optimal conditions were met. Each row was a timestamp for each minute the machine was running.
https://www.kaggle.com/datasets/programmer3/smart-manufacturing-process-data?resource=download

### Signals
I calculated the rolling means of the columns focusing on the machine's: temperature, speed, vibration, and energy. I printed out the rolling means for every 30 rows, which would be the mean for the previous 30 minutes that the machine was running.

### Experiments
I wanted to see how the machine held up over time. And since I had a larger data set, I wanted to see how the machine averaged for every 30 minutes. This I felt would smooth short-term variation without taking away from the data as a whole. This is why I set my window size to 30. I wanted to find the mean of the temperature, machine speed, vibration level, and energy consumption amounts. While I could have found the means of the production quality score and the optimal conditions score, I would not know why the machine was being rated the way that it was. Whereas if I find the mean of the different metrics, I am better able to understand how the machine is performing.

### Results
The temperature stayed between 74.48 and 75.60 degrees celsius. The speed in which the machine ran stayed between 1490.77 and 1508.07 RPMs, with most means over 1500. The vibrations were only either 0.06 or 0.07 mm/s which shows consistent, low vibration. And energy used ranged from 1.37 to 1.52 kilowatts per hour.

### Interpretation
This shows that throughout the morning, the machine stays pretty consistent. Even after 5 hours of use, the metrics are bouncing around within the stated range, not steadily increasing. Next steps would be to find the exact metrics determine if the machine is reaching its' optimal output and how to consistently reach those metrics.

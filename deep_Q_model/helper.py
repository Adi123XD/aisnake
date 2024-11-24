import matplotlib.pyplot as plt 
from IPython import display

plt.ion()
def plot(scores, mean_scores):
    display.clear_output(wait=True)
    display.display(plt.gcf())
    plt.clf()
    plt.title("Training...")
    plt.xlabel("Number of Games")
    plt.ylabel("Scores")
    plt.plot(scores, label="Scores")
    plt.plot(mean_scores, label="Mean Scores")
    plt.ylim(ymin=0)
    plt.text(len(scores) - 1, scores[-1], str(scores[-1]))
    plt.text(len(mean_scores) - 1, mean_scores[-1], str(mean_scores[-1]))
    plt.legend()
    plt.pause(0.1)  # Pause to display plot
"""
SOURCE
    https://cs50.harvard.edu/ai/2020/projects/2/pagerank/
    
SOLVED BY
    Diego Arnoldo Azuela Rosas

BACKGROUND
    When search engines like Google display search results, they do so by placing more “important” and higher-quality pages higher in the search results than less important pages. But how does the search engine know which pages are more important than other pages?
    One heuristic might be that an “important” page is one that many other pages link to, since it’s reasonable to imagine that more sites will link to a higher-quality webpage than a lower-quality webpage. We could therefore imagine a system where each page is given a rank according to the number of incoming links it has from other pages, and higher ranks would signal higher importance.
    But this definition isn’t perfect: if someone wants to make their page seem more important, then under this system, they could simply create many other pages that link to their desired page to artificially inflate its rank.
    For that reason, the PageRank algorithm was created by Google’s co-founders (including Larry Page, for whom the algorithm was named). In PageRank’s algorithm, a website is more important if it is linked to by other important websites, and links from less important websites have their links weighted less. This definition seems a bit circular, but it turns out that there are multiple strategies for calculating these rankings.

RANDOM SURFER MODEL
    One way to think about PageRank is with the random surfer model, which considers the behavior of a hypothetical surfer on the internet who clicks on links at random. Consider the corpus of web pages below, where an arrow between two pages indicates a link from one page to another.
    The random surfer model imagines a surfer who starts with a web page at random, and then randomly chooses links to follow. If the surfer is on Page 2, for example, they would randomly choose between Page 1 and Page 3 to visit next (duplicate links on the same page are treated as a single link, and links from a page to itself are ignored as well). If they chose Page 3, the surfer would then randomly choose between Page 2 and Page 4 to visit next.
    A page’s PageRank, then, can be described as the probability that a random surfer is on that page at any given time. After all, if there are more links to a particular page, then it’s more likely that a random surfer will end up on that page. Moreover, a link from a more important site is more likely to be clicked on than a link from a less important site that fewer pages link to, so this model handles weighting links by their importance as well.
    One way to interpret this model is as a Markov Chain, where each page represents a state, and each page has a transition model that chooses among its links at random. At each time step, the state switches to one of the pages linked to by the current state.
    By sampling states randomly from the Markov Chain, we can get an estimate for each page’s PageRank. We can start by choosing a page at random, then keep following links at random, keeping track of how many times we’ve visited each page. After we’ve gathered all of our samples (based on a number we choose in advance), the proportion of the time we were on each page might be an estimate for that page’s rank.
    However, this definition of PageRank proves slightly problematic, if we consider a network of pages like the below.
    Imagine we randomly started by sampling Page 5. We’d then have no choice but to go to Page 6, and then no choice but to go to Page 5 after that, and then Page 6 again, and so forth. We’d end up with an estimate of 0.5 for the PageRank for Pages 5 and 6, and an estimate of 0 for the PageRank of all the remaining pages, since we spent all our time on Pages 5 and 6 and never visited any of the other pages.
    To ensure we can always get to somewhere else in the corpus of web pages, we’ll introduce to our model a damping factor d. With probability d (where d is usually set around 0.85), the random surfer will choose from one of the links on the current page at random. But otherwise (with probability 1 - d), the random surfer chooses one out of all of the pages in the corpus at random (including the one they are currently on).
    Our random surfer now starts by choosing a page at random, and then, for each additional sample we’d like to generate, chooses a link from the current page at random with probability d, and chooses any page at random with probability 1 - d. If we keep track of how many times each page has shown up as a sample, we can treat the proportion of states that were on a given page as its PageRank.
ITERATIVE ALGORITHM
    We can also define a page’s PageRank using a recursive mathematical expression. Let PR(p) be the PageRank of a given page p: the probability that a random surfer ends up on that page. How do we define PR(p)? Well, we know there are two ways that a random surfer could end up on the page:
        1. With probability 1 - d, the surfer chose a page at random and ended up on page p.
        2. With probability d, the surfer followed a link from a page i to page p.
    The first condition is fairly straightforward to express mathematically: it’s 1 - d divided by N, where N is the total number of pages across the entire corpus. This is because the 1 - d probability of choosing a page at random is split evenly among all N possible pages.
    For the second condition, we need to consider each possible page i that links to page p. For each of those incoming pages, let NumLinks(i) be the number of links on page i. Each page i that links to p has its own PageRank, PR(i), representing the probability that we are on page i at any given time. And since from page i we travel to any of that page’s links with equal probability, we divide PR(i) by the number of links NumLinks(i) to get the probability that we were on page i and chose the link to page p.
    This gives us the following definition for the PageRank for a page p.
    In this formula, d is the damping factor, N is the total number of pages in the corpus, i ranges over all pages that link to page p, and NumLinks(i) is the number of links present on page i.
    How would we go about calculating PageRank values for each page, then? We can do so via iteration: start by assuming the PageRank of every page is 1 / N (i.e., equally likely to be on any page). Then, use the above formula to calculate new PageRank values for each page, based on the previous PageRank values. If we keep repeating this process, calculating a new set of PageRank values for each page based on the previous set of PageRank values, eventually the PageRank values will converge (i.e., not change by more than a small threshold with each iteration).
    In this project, you’ll implement both such approaches for calculating PageRank – calculating both by sampling pages from a Markov Chain random surfer and by iteratively applying the PageRank formula.

UNDERSTANDING
    Open up pagerank.py. Notice first the definition of two constants at the top of the file: DAMPING represents the damping factor and is initially set to 0.85. SAMPLES represents the number of samples we’ll use to estimate PageRank using the sampling method, initially set to 10,000 samples.
    Now, take a look at the main function. It expects a command-line argument, which will be the name of a directory of a corpus of web pages we’d like to compute PageRanks for. The crawl function takes that directory, parses all of the HTML files in the directory, and returns a dictionary representing the corpus. The keys in that dictionary represent pages (e.g., "2.html"), and the values of the dictionary are a set of all of the pages linked to by the key (e.g. {"1.html", "3.html"}).
    The main function then calls the sample_pagerank function, whose purpose is to estimate the PageRank of each page by sampling. The function takes as arguments the corpus of pages generated by crawl, as well as the damping factor and number of samples to use. Ultimately, sample_pagerank should return a dictionary where the keys are each page name and the values are each page’s estimated PageRank (a number between 0 and 1).
    The main function also calls the iterate_pagerank function, which will also calculate PageRank for each page, but using the iterative formula method instead of by sampling. The return value is expected to be in the same format, and we would hope that the output of these two functions should be similar when given the same corpus!

SPECIFICATION
    Complete the implementation of transition_model, sample_pagerank, and iterate_pagerank.
    The transition_model should return a dictionary representing the probability distribution over which page a random surfer would visit next, given a corpus of pages, a current page, and a damping factor.
        The function accepts three arguments: corpus, page, and damping_factor.
            The corpus is a Python dictionary mapping a page name to a set of all pages linked to by that page.
            The page is a string representing which page the random surfer is currently on.
            The damping_factor is a floating point number representing the damping factor to be used when generating the probabilities.
        The return value of the function should be a Python dictionary with one key for each page in the corpus. Each key should be mapped to a value representing the probability that a random surfer would choose that page next. The values in this returned probability distribution should sum to 1.
            With probability damping_factor, the random surfer should randomly choose one of the links from page with equal probability.
            With probability 1 - damping_factor, the random surfer should randomly choose one of all pages in the corpus with equal probability.
        For example, if the corpus were {"1.html": {"2.html", "3.html"}, "2.html": {"3.html"}, "3.html": {"2.html"}}, the page was "1.html", and the damping_factor was 0.85, then the output of transition_model should be {"1.html": 0.05, "2.html": 0.475, "3.html": 0.475}. This is because with probability 0.85, we choose randomly to go from page 1 to either page 2 or page 3 (so each of page 2 or page 3 has probability 0.425 to start), but every page gets an additional 0.05 because with probability 0.15 we choose randomly among all three of the pages.
        If page has no outgoing links, then transition_model should return a probability distribution that chooses randomly among all pages with equal probability. (In other words, if a page has no links, we can pretend it has links to all pages in the corpus, including itself.)
    The sample_pagerank function should accept a corpus of web pages, a damping factor, and a number of samples, and return an estimated PageRank for each page.
        The function accepts three arguments: corpus, a damping_factor, and n.
            The corpus is a Python dictionary mapping a page name to a set of all pages linked to by that page.
            The damping_factor is a floating point number representing the damping factor to be used by the transition model.
            n is an integer representing the number of samples that should be generated to estimate PageRank values.
        The return value of the function should be a Python dictionary with one key for each page in the corpus. Each key should be mapped to a value representing that page’s estimated PageRank (i.e., the proportion of all the samples that corresponded to that page). The values in this dictionary should sum to 1.
        The first sample should be generated by choosing from a page at random.
        For each of the remaining samples, the next sample should be generated from the previous sample based on the previous sample’s transition model.
            You will likely want to pass the previous sample into your transition_model function, along with the corpus and the damping_factor, to get the probabilities for the next sample.
            For example, if the transition probabilities are {"1.html": 0.05, "2.html": 0.475, "3.html": 0.475}, then 5% of the time the next sample generated should be "1.html", 47.5% of the time the next sample generated should be "2.html", and 47.5% of the time the next sample generated should be "3.html".
        You may assume that n will be at least 1.
    The iterate_pagerank function should accept a corpus of web pages and a damping factor, calculate PageRanks based on the iteration formula described above, and return each page’s PageRank accurate to within 0.001.
        The function accepts two arguments: corpus and damping_factor.
            The corpus is a Python dictionary mapping a page name to a set of all pages linked to by that page.
            The damping_factor is a floating point number representing the damping factor to be used in the PageRank formula.
        The return value of the function should be a Python dictionary with one key for each page in the corpus. Each key should be mapped to a value representing that page’s PageRank. The values in this dictionary should sum to 1.
        The function should begin by assigning each page a rank of 1 / N, where N is the total number of pages in the corpus.
        The function should then repeatedly calculate new rank values based on all of the current rank values, according to the PageRank formula in the “Background” section. (i.e., calculating a page’s PageRank based on the PageRanks of all pages that link to it).
            A page that has no links at all should be interpreted as having one link for every page in the corpus (including itself).
        This process should repeat until no PageRank value changes by more than 0.001 between the current rank values and the new rank values.
    You should not modify anything else in pagerank.py other than the three functions the specification calls for you to implement, though you may write additional functions and/or import other Python standard library modules. You may also import numpy or pandas, if familiar with them, but you should not use any other third-party Python modules.

HINTS
    - You may find the functions in Python’s random module helpful for making decisions pseudorandomly.

IMPROVEMENTS
    - There are 2 versions of the function 'iterate_pagerank(corpus, damping_factor)' must review to eliminate the second one, the first one does not work at the moment. 

"""
# SOURCE: https://plcoster.github.io/homepage/cs50ai_projects.html

import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability 'damping_factor', choose a link at random
    linked to by 'page'. With probability '1 - damping_factor', choose
    a link at random chosen from all pages in the corpus.
    """
    # Initialize the dictionary to be returned
    dict_probDist = {page_name: 0 for page_name in corpus}

    # If page has no outgoing links, we can pretend it has links to all pages in the corpus, including itself.
    if len(corpus[page]) == 0:
        for page_name in dict_probDist:
            dict_probDist[page_name] = 1 / len(corpus)
        return dict_probDist

    # With probability [damping_factor], the random surfer should randomly choose one of the links from page with equal probability.
    prob_LinkPage = ( (damping_factor) / len(corpus[page]) )

    # With probability [1 - damping_factor], the random surfer should randomly choose one of all pages in the corpus with equal probability.
    prob_LinkCorpus = ( (1 - damping_factor) / (len(corpus)) )

    # Create dictionary with correct probabilities  
    for page_name in dict_probDist:
        dict_probDist[page_name] += prob_LinkCorpus
        if page_name in corpus[page]:
            dict_probDist[page_name] += prob_LinkPage

    return dict_probDist # {pageName:pageProb}


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling 'n' pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # Create a dictionary based on the visit to each page
    dict_pageVisit = {page_name: 0 for page_name in corpus}

    # The return value of the function should be a Python dictionary with one key for each page mapped to a value representing that page’s estimated PageRank.

    # The first sample [n==1] should be generated by choosing from a page at random
    current_Page = random.choice(list(dict_pageVisit)) #Dont need to specify the page?
    dict_pageVisit[current_Page] += 1

    # For each of the remaining samples [n-1], the next sample should be generated from the previous sample based on the previous sample’s transition model. 
    for i in range(0, n-1): #Start from 1 to avoid double-counting the already created sample
        transitionModel = transition_model(corpus, current_Page, damping_factor) # {pageName:pageProb}
        # Next sample should be generated from the previous sample based on the previous sample’s transition model.
        current_Page = random.choice(list(transitionModel.keys()))
        dict_pageVisit[current_Page] += 1

    # Normalize visits using sample number
    estimate_PageRank = {page_name : (num_visits/n) for page_name, num_visits in dict_pageVisit.items()}
    print('Estimate sum of probabilities (must be equal to 1) is: ', round(sum(estimate_PageRank.values()),4))

    return estimate_PageRank #{pageName:PageRank}


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # Calculate static values for future uses
    initial_rank, rand_choiceProb, counter = 1/(len(corpus)), ((1-damping_factor)/(len(corpus))), 0

    # The function should begin by assigning each page a rank of 1 / N, where N is the total number of pages in the corpus.
    dict_pageRank = {page_name: initial_rank for page_name in corpus}
    dict_newRank = {page_name: None for page_name in corpus}
    max_deltaRank = initial_rank

    # This process should repeat until no PageRank value changes by more than 0.001 between the current rank values and the new rank values
    while max_deltaRank > 0.001:
        max_deltaRank = 0

        # Calculate new rank values based on all of the current rank values, according to the PageRank formula in the “Background” 
        for page_name in corpus:

            # Name of the model [found in 'Background']
            rand_surferModel = 0 
            for page_name_2 in corpus:

                # A page that has no links at all should be interpreted as having one link for every page in the corpus (including itself).
                if len(corpus[page_name_2]) == 0:
                    rand_surferModel += dict_pageRank[page_name_2] * initial_rank

                # Page_name within the page, means that it randomly picks a page from those options
                elif page_name in corpus[page_name_2]:
                    rand_surferModel += dict_pageRank[page_name_2] / len(corpus[page_name_2])
                    
            # Calculate the PageRank based on the formula provided in 'Background'
            new_rank = rand_choiceProb + (damping_factor * rand_surferModel)
            dict_newRank[page_name] = new_rank

        # Normalize the results obtained
        normalized_factor = sum(dict_newRank.values())
        dict_newRank = {page: (rank/normalized_factor) for page, rank in dict_newRank.items()}

        # Find delta in PageRank
        for page_name in corpus:
            deltaRank = abs(dict_pageRank[page_name] - dict_newRank[page_name])
            if deltaRank > max_deltaRank:
                max_deltaRank = deltaRank

        # Update PageRanks
        estimate_PageRank = dict_newRank.copy()

    # The return value of the function should be a Python dictionary with one key for each page mapped to a value representing that page’s PageRank.
    print('Estimate sum of probabilities (must be equal to 1): ', round(sum(estimate_PageRank.values()),4))

    return estimate_PageRank #{pageName:PageRank}


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.
    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # Calculate some constants from the corpus for further use:
    num_pages = len(corpus)
    init_rank = 1 / num_pages
    random_choice_prob = (1 - damping_factor) / len(corpus)
    iterations = 0

    # Initial page_rank gives every page a rank of 1/(num pages in corpus)
    page_ranks = {page_name: init_rank for page_name in corpus}
    new_ranks = {page_name: None for page_name in corpus}
    max_rank_change = init_rank

    # Iteratively calculate page rank until no change > 0.001
    while max_rank_change > 0.001:

        iterations += 1
        max_rank_change = 0

        for page_name in corpus:
            surf_choice_prob = 0
            for other_page in corpus:
                # If other page has no links it picks randomly any corpus page:
                if len(corpus[other_page]) == 0:
                    surf_choice_prob += page_ranks[other_page] * init_rank
                # Else if other_page has a link to page_name, it randomly picks from all links on other_page:
                elif page_name in corpus[other_page]:
                    surf_choice_prob += page_ranks[other_page] / len(corpus[other_page])
            # Calculate new page rank
            new_rank = random_choice_prob + (damping_factor * surf_choice_prob)
            new_ranks[page_name] = new_rank

        # Normalize the new page ranks:
        norm_factor = sum(new_ranks.values())
        new_ranks = {page: (rank / norm_factor) for page, rank in new_ranks.items()}

        # Find max change in page rank:
        for page_name in corpus:
            rank_change = abs(page_ranks[page_name] - new_ranks[page_name])
            if rank_change > max_rank_change:
                max_rank_change = rank_change

        # Update page ranks to the new ranks:
        page_ranks = new_ranks.copy()

    print('Iteration took', iterations, 'iterations to converge')
    print('Sum of iteration page ranks: ', round(sum(page_ranks.values()), 4))

    return page_ranks

if __name__ == "__main__":
    main()
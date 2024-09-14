import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


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
        pages[filename] = set(link for link in pages[filename] if link in pages)

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    total_pages = len(corpus)
    linked_pages = corpus[page]
    all_pages_p = (1 - damping_factor) / total_pages

    if len(linked_pages) > 0:
        probability_distribution = dict.fromkeys(corpus.keys(), all_pages_p)
        for link in linked_pages:
            probability_distribution[link] += damping_factor / len(linked_pages)

    if len(linked_pages) == 0:
        probability_distribution = dict.fromkeys(corpus.keys(), 1 / total_pages)

    return probability_distribution


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """

    page_rank = {page: 0 for page in corpus}
    keys = list(corpus.keys())
    r = random.randrange(0, len(keys))
    random_page = keys[r]

    for _ in range(n):
        page_rank[random_page] += 1
        sample = transition_model(corpus, random_page, damping_factor)

        random_page = random.choices(list(sample.keys()), list(sample.values()))[0]

    page_rank = {page: value / n for page, value in page_rank.items()}

    print(page_rank)
    return page_rank


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    N = len(corpus)
    initial_rank = 1 / N
    pageranks = {page: initial_rank for page in corpus}

    new_ranks = pageranks.copy()

    converged = False
    while not converged:
        converged = True

        for page in corpus:
            rank_sum = 0
            for linking_page in corpus:
                if corpus[linking_page]:
                    if page in corpus[linking_page]:
                        rank_sum += pageranks[linking_page] / len(corpus[linking_page])
                else:
                    rank_sum += pageranks[linking_page] / N

            new_rank = (1 - damping_factor) / N + damping_factor * rank_sum
            new_ranks[page] = new_rank

        for page in pageranks:
            if abs(new_ranks[page] - pageranks[page]) >= 0.0001:
                converged = False

        pageranks = new_ranks.copy()

    return pageranks


if __name__ == "__main__":
    main()

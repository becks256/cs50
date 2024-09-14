import csv
import itertools
import sys

PROBS = {
    # Unconditional probabilities for having gene
    "gene": {2: 0.01, 1: 0.03, 0: 0.96},
    "trait": {
        # Probability of trait given two copies of gene
        2: {True: 0.65, False: 0.35},
        # Probability of trait given one copy of gene
        1: {True: 0.56, False: 0.44},
        # Probability of trait given no gene
        0: {True: 0.01, False: 0.99},
    },
    # Mutation probability
    "mutation": 0.01,
}


def main():

    # Check for proper usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python heredity.py data.csv")
    people = load_data(sys.argv[1])

    # Keep track of gene and trait probabilities for each person
    probabilities = {
        person: {"gene": {2: 0, 1: 0, 0: 0}, "trait": {True: 0, False: 0}}
        for person in people
    }

    # Loop over all sets of people who might have the trait
    names = set(people)
    for have_trait in powerset(names):

        # Check if current set of people violates known information
        fails_evidence = any(
            (
                people[person]["trait"] is not None
                and people[person]["trait"] != (person in have_trait)
            )
            for person in names
        )
        if fails_evidence:
            continue

        # Loop over all sets of people who might have the gene
        for one_gene in powerset(names):
            for two_genes in powerset(names - one_gene):

                # Update probabilities with new joint probability
                p = joint_probability(people, one_gene, two_genes, have_trait)
                update(probabilities, one_gene, two_genes, have_trait, p)

    # Ensure probabilities sum to 1
    normalize(probabilities)

    # Print results
    for person in people:
        print(f"{person}:")
        for field in probabilities[person]:
            print(f"  {field.capitalize()}:")
            for value in probabilities[person][field]:
                p = probabilities[person][field][value]
                print(f"    {value}: {p:.4f}")


def load_data(filename):
    """
    Load gene and trait data from a file into a dictionary.
    File assumed to be a CSV containing fields name, mother, father, trait.
    mother, father must both be blank, or both be valid names in the CSV.
    trait should be 0 or 1 if trait is known, blank otherwise.
    """
    data = dict()
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            data[name] = {
                "name": name,
                "mother": row["mother"] or None,
                "father": row["father"] or None,
                "trait": (
                    True
                    if row["trait"] == "1"
                    else False if row["trait"] == "0" else None
                ),
            }
    return data


def powerset(s):
    """
    Return a list of all possible subsets of set s.
    """
    s = list(s)
    return [
        set(s)
        for s in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1)
        )
    ]


def joint_probability(people, one_gene, two_genes, have_trait):
    """
    Compute and return a joint probability.

    The probability returned should be the probability that
        * everyone in set `one_gene` has one copy of the gene, and
        * everyone in set `two_genes` has two copies of the gene, and
        * everyone not in `one_gene` or `two_gene` does not have the gene, and
        * everyone in set `have_trait` has the trait, and
        * everyone not in set` have_trait` does not have the trait.
    """

    """
    # Unconditional probability is defined as the degree of belief in a proposition in the absence of any evidence.

    # Conditional probability is defined as the degree of belief in a proposition given some evidence that has already been revealed

    # Unconditional probabilities for having gene
    "gene": {2: 0.01, 1: 0.03, 0: 0.96},
    "trait": {
        # Probability of trait given two copies of gene
        2: {True: 0.65, False: 0.35},
        # Probability of trait given one copy of gene
        1: {True: 0.56, False: 0.44},
        # Probability of trait given no gene
        0: {True: 0.01, False: 0.99},
    },
    # Mutation probability
    "mutation": 0.01,

    P(a | b) : Probability of a given b
    calculating conditional probability = P(a | b) = P(a and b) / P(b) OR P(a and b) = P(b)P(a | b)

    gene = random variable

    probability of having gene given no parents have gene = 0.01
    probability of having gene given one parent has gene = 0.03
    probability of having gene given both parents have gene = 0.96

    """

    probability = 1

    for person in people:
        # determine the number of genes the person has
        genes = 2 if person in two_genes else 1 if person in one_gene else 0

        # determine if the person has the trait
        trait = person in have_trait

        if people[person]["mother"] is None:
            # if the person has no parents, use the unconditional probability
            gene_prob = PROBS["gene"][genes]
        else:
            # otherwise, calculate the probability based on the parents genes
            mother = people[person]["mother"]
            father = people[person]["father"]

            # calculate the probability of inheriting the gene from each parent
            passing_prob = {
                mother: (
                    1 - PROBS["mutation"]
                    if mother in two_genes
                    else 0.5 if mother in one_gene else PROBS["mutation"]
                ),
                father: (
                    1 - PROBS["mutation"]
                    if father in two_genes
                    else 0.5 if father in one_gene else PROBS["mutation"]
                ),
            }

            if genes == 2:
                # if the person has two genes, calculate the probability they inherited one from each parent
                gene_prob = passing_prob[mother] * passing_prob[father]
            elif genes == 1:
                # if the person has one gene, calculate the probability they inherited the gene from one parent, but not the other
                gene_prob = (
                    passing_prob[mother] * (1 - passing_prob[father])
                    + (1 - passing_prob[mother]) * passing_prob[father]
                )
            else:
                # otherwise, its the probability of getting no genes from both parents
                gene_prob = (1 - passing_prob[mother]) * (1 - passing_prob[father])

        # calculate the probability of the person having the trait given their genes
        trait_prob = PROBS["trait"][genes][trait]
        probability *= gene_prob * trait_prob

    return probability


def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """

    for person in probabilities:
        genes = 2 if person in two_genes else 1 if person in one_gene else 0

        trait = person in have_trait

        # Update gene probability
        probabilities[person]["gene"][genes] += p
        # Update trait probability
        probabilities[person]["trait"][trait] += p


def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """

    for person in probabilities:
        # Normalize gene probabilities
        gene_total = sum(probabilities[person]["gene"].values())
        for gene in probabilities[person]["gene"]:
            probabilities[person]["gene"][gene] /= gene_total

        # Normalize trait probabilities
        trait_total = sum(probabilities[person]["trait"].values())
        for trait in probabilities[person]["trait"]:
            probabilities[person]["trait"][trait] /= trait_total


if __name__ == "__main__":
    main()

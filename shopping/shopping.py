import csv
import sys
import datetime

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")


def load_data(filename):
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).

    evidence should be a list of lists, where each list contains the
    following values, in order:
        - Administrative, an integer
        - Administrative_Duration, a floating point number
        - Informational, an integer
        - Informational_Duration, a floating point number
        - ProductRelated, an integer
        - ProductRelated_Duration, a floating point number
        - BounceRates, a floating point number
        - ExitRates, a floating point number
        - PageValues, a floating point number
        - SpecialDay, a floating point number
        - Month, an index from 0 (January) to 11 (December)
        - OperatingSystems, an integer
        - Browser, an integer
        - Region, an integer
        - TrafficType, an integer
        - VisitorType, an integer 0 (not returning) or 1 (returning)
        - Weekend, an integer 0 (if false) or 1 (if true)

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """

    def get_month(m):
        if m == "June":
            m = "Jun"
        date_obj = datetime.datetime.strptime(m, "%b")
        return date_obj.month - 1

    def get_visitor_type(v):
        if v == "Returning_Visitor":
            return 1
        else:
            return 0

    def get_weekend(w):
        if w == "TRUE":
            return 1
        else:
            return 0

    type_map = {
        0: int,  # Administrative, an integer
        1: float,  # Administrative_Duration, a floating point number
        2: int,  # Informational, an integer
        3: float,  # Informational_Duration, a floating point number
        4: int,  # ProductRelated, an integer
        5: float,  # ProductRelated_Duration, a floating point number
        6: float,  # BounceRates, a floating point number
        7: float,  # ExitRates, a floating point number
        8: float,  # PageValues, a floating point number
        9: float,  # SpecialDay, a floating point number
        10: get_month,  # Month, an index from 0 (January) to 11 (December)
        11: int,  # OperatingSystems, an integer
        12: int,  # Browser, an integer
        13: int,  # Region, an integer
        14: int,  # TrafficType, an integer
        15: get_visitor_type,  # VisitorType, an integer 0 (not returning) or 1 (returning)
        16: get_weekend,  # Weekend, an integer 0 (if false) or 1 (if true)
    }

    def convert_value(value, expected_type):
        try:
            return expected_type(value)
        except ValueError:
            raise TypeError(
                f"Value '{value}' cannot be converted to {expected_type.__name__}"
            )

    with open(filename) as f:
        reader = csv.reader(f)
        header = next(reader)

        headers = {headers: index for index, headers in enumerate(header)}

        evidence = []
        labels = []
        for row in reader:
            converted_row = []
            for index, value in enumerate(row):
                if index == len(headers) - 1:
                    break

                expected_type = type_map[index]
                converted_value = convert_value(value, expected_type)
                converted_row.append(converted_value)

            evidence.append(converted_row)
            labels.append(1 if row[headers["Revenue"]] == "TRUE" else 0)

        # print(evidence[:3])
        # print(labels[:3])
        return evidence, labels


def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """

    model = KNeighborsClassifier(n_neighbors=1)
    model.fit(evidence, labels)

    return model


def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificity).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """

    true_positive = 0
    true_negative = 0
    false_negative = 0
    false_positive = 0

    for actual, predicted in zip(labels, predictions):
        if actual == 1:
            if predicted == 1:
                true_positive += 1
            else:
                false_negative += 1
        else:
            if predicted == 0:
                true_negative += 1
            else:
                false_positive += 1

    
    sensitivity = true_positive / (true_positive + false_negative)
    specificity = true_negative / (true_negative + false_positive)

    return sensitivity, specificity


if __name__ == "__main__":
    main()

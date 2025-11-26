from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
import numpy as np

def print_stacktrace(e: Exception):
    import traceback    
    import sys    
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def main():
    doc = ['some fake text that is fake to test the vectorizer']

    # Create a CountVectorizer and fit it
    cv = CountVectorizer()
    cv.fit(doc)

    # Create a TfidfTransformer and fit it
    tf = TfidfTransformer()
    tf.fit(cv.transform(doc))

    # Try to recreate the CountVectorizer
    cv_recreated = CountVectorizer()
    cv_recreated.set_params(**cv.get_params())
    cv_recreated.set_params(**{'vocabulary': cv.vocabulary_})
    m1 = cv.transform(doc)
    m2 = cv_recreated.transform(doc)
    assert np.array_equal(m1.todense(), m2.todense())

    # Try to recreate the TfidfTransformer
    tf_recreated = TfidfTransformer()
    tf_recreated.set_params(**tf.get_params())
    try:
        tf_recreated.idf_ = tf.idf_
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Cannot set idf_ attribute")

if __name__ == "__main__":
    main()

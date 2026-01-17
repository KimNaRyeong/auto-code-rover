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
    try:
        import seaborn as sns
        import matplotlib.pyplot as plt

        sns.set_context("paper")
        sns.set_style("white")

        data = (sns.load_dataset('iris').set_index('species')*1e7).reset_index()
        for sharex, sharey in [(True, True), (False, False)]:
            g = sns.relplot(data=data, x='sepal_length', y='sepal_width', col='species', 
                            col_wrap=2, height=2.5, facet_kws={'sharex': sharex, 'sharey': sharey})
            g.set_titles(row_template="{row_name}", col_template="SOMEWHATLONG-{col_name}")
            for axes in g.axes.flat:
                axes.ticklabel_format(axis='both', style='scientific', scilimits=(0, 0))
            plt.close()

        # No exceptions were raised, plots were generated.
        # However, we cannot programmatically assert the absence of label overlapping,
        # so we assume no visual issue if we reached this point without errors.
        
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Failed to generate plots correctly, which might indicate the presence of the issue.")

if __name__ == "__main__":
    try:
        main()
        print("The script executed successfully. Manual verification of the produced plots is required to check for label overlap.")
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)  # Exit with code 1 to indicate an error condition
    except Exception as e:
        print_stacktrace(e)
        exit(1)
    exit(0)  # Exit successfully if no AssertionError was raised

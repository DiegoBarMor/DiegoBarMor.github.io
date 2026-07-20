import pandas as pd
from pathlib import Path
from collections import Counter
import matplotlib.pyplot as plt
import seaborn as sns

RELEVANT_AUTHORS = [
    "DBM", "Diego", "Diego BM", "Diego Barquero Morera", "DiegoBarMor", "DiegoBarqueroMorera",
]

RELEVANT_EXTENSIONS = {
    "python" : ["py", "pyw", "ipynb"],
    "bash" : ["sh"],
    "html/js/css" : ["htm", "html", "css", "js"],
    "fortran" : ["f", "f90", "F90"],
    "c" : ["c", "h"],
    "cpp" : ["cpp", "hpp"],
    "csharp" : ["cs"],
    "java/kotlin" : ["java", "kt", "kts"],
    "rust" : ["rs"],
}

KNOWN_LANGUAGES = {
    ext: language
    for language,exts in RELEVANT_EXTENSIONS.items()
    for ext in exts
}

# ------------------------------------------------------------------------------
def parse_changes(raw: str) -> str:
    changes = filter(
        lambda change: change[0] in ("A", "M"), # consider only files that were added or modified
        (change.split("//") for change in raw.split("///"))
    )
    extensions = filter(None,
        (Path(change[1]).suffix for change in changes)
    )
    return ';'.join(ext[1:] for ext in extensions)


# ------------------------------------------------------------------------------
def parse_extensions(raw: pd.Series) -> dict[str, int]:
    extensions = (ext for exts in raw for ext in exts.split(";"))
    languages = filter(None, (KNOWN_LANGUAGES.get(ext) for ext in extensions))
    count = Counter(languages)
    return {
        language: count.get(language, 0)
        for language in RELEVANT_EXTENSIONS.keys()
    }


# ------------------------------------------------------------------------------
def main():
    df = pd.read_csv(PATH_CSV_REPOS)

    ### PART 0: inspect all commit authors present in the repos summary
    # all_authors = df["author"].unique()
    # print(*sorted(all_authors), sep = '\n')


    ### PART 1: filter the repos summary to only include the repos that have specific author
    author_names = df["author"].map(lambda s: s.split(" <")[0])
    df = df[author_names.isin(RELEVANT_AUTHORS)]
    # print(sorted(df["author"].unique()))
    # df.to_csv(PATH_CSV_REPOS, index = False) # optional


    ### PART 2: parse the changes column to extract the file extensions of the files that were added or modified
    df["year_month"] = df["date"].map(lambda s: '/'.join(s.split("/")[:2]))
    df["extensions"] = df["changes"].map(parse_changes)
    df = df[["year_month", "extensions"]]
    df = df[df["extensions"] != ""]
    # print(df)

    # all_extensions = set(ext for exts in df["extensions"] for ext in exts.split(";"))
    # print(sorted(all_extensions))


    ### PART 3: group the repos summary by year/month and file extension, and count the number of occurrences
    df_stats = pd.DataFrame([
        {"year_month": year_month, **parse_extensions(df[df["year_month"] == year_month]["extensions"])}
        for year_month in df["year_month"].unique()
    ])
    df_stats.sort_values("year_month", inplace = True)
    print(df_stats)


    ### PART 4: plot the number of occurrences of each file extension per month
    sns.color_palette("colorblind")
    sns.lineplot(
        data = df_stats.melt(id_vars = "year_month", var_name = "language", value_name = "count"),
        x = "year_month", y = "count", hue = "language", style = "language", markers = True, dashes = False,
    )

    year  = df_stats["year_month"].map(lambda s: s.split("/")[0])
    month = df_stats["year_month"].map(lambda s: s.split("/")[1])
    c_years = sorted(Counter(year).items(), key = lambda t: t[0])
    xpos = 0
    for year,n_months in c_years:
        xpos += n_months
        plt.axvline(x = xpos - 0.5, color = "gray", linestyle = "--", linewidth = 1.0)
        plt.text(x = xpos - n_months/2 - 0.5, y = plt.ylim()[1] - 25, s = year, fontsize = 16, ha = "center", va = "bottom")

    plt.legend(loc = "center left", fontsize = 16)
    plt.title("Number of files modified/added per month by language", fontsize = 18)
    plt.ylabel("# of files modified/added", fontsize = 16)
    plt.xlabel("Month", fontsize = 16)
    plt.xticks(ticks = range(len(df_stats)), labels = month, rotation = 60)
    plt.tick_params(axis = "both", which = "major", labelsize = 14)
    plt.show()


################################################################################
if __name__ == "__main__":
    PATH_CSV_REPOS = Path("utils/repos.csv") # repos summary produced by "hongsamut gitsummary"
    main()


################################################################################
# python3 utils/stats_languages.py

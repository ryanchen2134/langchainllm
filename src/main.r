library(googlesheets4)
library(tidyverse)
library(reticulate)
use_virtualenv("../../")
source_python("funs.py")

dat <- read_sheet("SHEET_ID_GOES_HERE") %>%
  mutate(film = as.character(film)) %>%
  select(year, film) %>%
  mutate(resp = NA)

for (r in 1:nrow(dat)) {
    cat("prompting", r, "\n")
    dat$resp[r] <- str_replace_all( 
        prior_films(dat$year[r], dat$film[r]),
        fixed("\n"),
        " " 
    )

    cat("writing", r, "\n")
    if (r == 1) {
        write_csv(dat[r, ], "prior_films.csv")
    } else {
        write_csv(dat[r, ], "prior_films.csv", append = TRUE)
    }

    Sys.sleep(runif(1, 2, 10))
}
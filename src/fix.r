library(googlesheets4) # provides oauth browser implementation
library(tidyverse)
library(reticulate) # provides access to python

source_python("./src/main.py")
use_virtualenv("./venv")
#read google sheet with year, film format
dat <- read_sheet("1-y3-3wSL8p12kGCF0Qqgl6I1aGSex0nrkdLLytN5eoA") %>%
  mutate(film = as.character(film)) %>%
  select(year, film) %>%
  mutate(resp = NA)

for (r in 1:nrow(dat)) {
    if (dat$resp[r] == "Agent stopped due to max iterations.") {
        cat("Re-prompting for row", r, "\n")

        dat$resp[r] <- str_replace_all( 
            prior_films(dat$year[r], dat$film[r]), 
            fixed("\n"),
            " " 
        )

        cat("Writing row", r, "\n")
        if (r == 1) {  
            write_csv(dat[r, ], "prior_films.csv")
        } else {
            write_csv(dat[r, ], "prior_films.csv", append = TRUE)
        }
    }

    

    Sys.sleep(runif(1, 2, 10))
}
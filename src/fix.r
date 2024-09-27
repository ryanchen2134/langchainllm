
library(tidyverse)
library(reticulate) # provides access to python

source_python("./src/main.py")
use_virtualenv("./venv")
#read google sheet with year, film format
dat <- read_csv("prior_films.csv") |>
  select(year, film, resp) 

for (r in 1:nrow(dat)) {
    if (dat$resp[r] == "Agent stopped due to max iterations.") {
        cat("Re-prompting for row", r, "\n")

        dat$resp[r] <- str_replace_all( 
            prior_films(dat$year[r], dat$film[r]), 
            fixed("\n"),
            " " 
        )

        cat("Writing row", r, "\n")
        dat$resp[r] |> cat("\n")

        write_csv(dat, "prior_films.csv")

    }
    Sys.sleep(runif(1, 2, 10))
}
library(tidyverse)

dat <- read_csv("prior_films.csv")

dat <- dat %>% 
  mutate(
    resp_clean = case_when(
      str_detect(tolower(resp), "the number(.*)is") ~ 
        str_split_i(tolower(resp), "the number(.*)is", 2)
    ),
    resp_clean = str_remove_all(resp_clean, "[^0-9]")
  )

# manual code the rest
lgl <- !is.na(dat$resp) & 
  dat$resp != "Agent stopped due to max iterations." &
  is.na(dat$resp_clean)

dat$resp[lgl] # read with mine own human eyes
dat$resp_clean[lgl] <- c(NA, NA, 44, NA, NA,
                         NA, NA, NA, NA, NA,
                         4,  NA, NA, 86, NA,
                         9,  NA,  4, 33, 26)
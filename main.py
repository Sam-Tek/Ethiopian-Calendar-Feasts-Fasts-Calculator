#!/usr/bin/env python3
"""
Calculation of holiday and fast dates according to the Ethiopian calendar.
The Ethiopian calendar has 12 months of 30 days each and a 13th month, Pagumen,
composed of 5 days (6 in leap years).

This script does not depend on the Gregorian calendar: all operations are performed
on the Ethiopian calendar only.
"""

from dataclasses import dataclass
import math

# --- Definitions of Ethiopian months ---
MONTHS = [
    "Mäskäräm", "Teqemt", "Hedar", "Tahesas", "Ter", "Yäkatit",
    "Mägabit", "Miyazya", "Guenbot", "Säné", "Hamlé", "Nähasé", "Pagumén"
]

EVANGELISTS = ["John", "Matthew", "Mark", "Luke"]
DAYSFORJOHN = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
ADDON = [6, 5, 4, 3, 2, 8, 7]  # Correspond à l'ajout pour Mebega Hemere selon le jour

@dataclass
class EthioDate:
    year: int
    month: int
    day: int

    def __repr__(self):
        return f"{self.day} {MONTHS[self.month-1]} {self.year}"


def is_ethio_leap(year: int) -> bool:
    """Determines if an Ethiopian year is a leap year (every 4 years)."""
    return (year % 4) == 3


def month_length(month: int, year: int) -> int:
    if 1 <= month <= 12:
        return 30
    elif month == 13:
        return 6 if is_ethio_leap(year) else 5
    else:
        raise ValueError("Invalid month (1-13 expected)")


def add_days(date: EthioDate, days: int) -> EthioDate:
    year, month, day = date.year, date.month, date.day
    if days >= 0:
        while days > 0:
            ml = month_length(month, year)
            if day + days <= ml:
                day += days
                days = 0
            else:
                days -= (ml - day + 1)
                day = 1
                month += 1
                if month > 13:
                    month = 1
                    year += 1
    return EthioDate(year, month, day)


def add_months(date: EthioDate, months: int) -> EthioDate:
    total_months = (date.month - 1) + months
    new_year = date.year + total_months // 13
    new_month = (total_months % 13) + 1
    new_day = min(date.day, month_length(new_month, new_year))
    return EthioDate(new_year, new_month, new_day)


def compute_fasts_and_feasts(year: int):
    """Calculates all feasts and fasts from a given Ethiopian year."""
    yw = 5500 + year

    # Get the last two digits of the year
    last_two_digits = year % 100

    #Use the last two digits for calculations
    E = math.trunc(last_two_digits % 4)
    Mr = math.trunc(yw / 4)
    Jd = math.trunc((Mr + yw) % 7)
    c = math.trunc(yw % 19)
    c = 19 if c == 0 else c
    n = c - 1
    a = math.trunc((n * 11) % 30)
    m = 30 - a

    # Determination of the Feast of Trumpets
    if m < 14:
        t_month, t_day = 2, m  # Teqemt
    else:
        t_month, t_day = 1, m  # Mäskäräm

    t_date = EthioDate(year, t_month, t_day)

    #get day of week from t_date
    first_day_index = Jd
    if (t_month == 2):
        first_day_index = (first_day_index + 2) % 7
    for i in range(t_day):
        t_day_index = (first_day_index + i) % 7

        
        

    # Mebega Hemere = feast of trumpets + addon
    h_date = add_days(t_date, ADDON[t_day_index])

    # Nineveh = +4 months
    nineveh = add_months(h_date, 4)

    # List of festivals and fasts according to offsets
    offsets = {
        'Great Lent': 14,
        'Mt Olivier': 41,
        'Hosanna': 62,
        'Crucifixion': 67,
        'Resurrection': 69,
        'Synod': 93,
        'Ascension': 108,
        'Pentecost': 118,
        'Fast of Holy Apostles': 119,
        'Salvation Fast': 121
    }

    results = {
        'Ethiopian Year': year,
        'YW': yw,
        'Evangelist (E)': str(E)+' '+str(EVANGELISTS[E]),
        'Metene Rabeite (Mr)': Mr,
        'Day of John (Jd)': str(Jd)+' '+str(DAYSFORJOHN[Jd]),
        'Cycle (c)': c,
        'Golden number (n)': n,
        'Epact (a)': a,
        'm': m,
        'Beale Meteque (Feast of Trumpet)': str(t_date)+' '+str(DAYSFORJOHN[t_day_index]),
        'Mebega Hemere (Ark’s dwelling place)': str(h_date)+' ADDON: '+str(ADDON[t_day_index]),
        'Nineveh': nineveh
    }
    results = {
        'Ethiopian Year': year,
        'YW': yw,
        'Evangelist (E)': f"{E} {EVANGELISTS[E]}",
        'Metene Rabeite (Mr)': Mr,
        'Day of John (Jd)': f"{Jd} {DAYSFORJOHN[Jd]}",
        'Cycle (c)': c,
        'Golden number (n)': n,
        'Epact (a)': a,
        'm': m,
        'Beale Meteque (Feast of Trumpet)': f"{t_date} {DAYSFORJOHN[t_day_index]}",
        'Mebega Hemere (Ark’s dwelling place)': f"{h_date} ADDON: {ADDON[t_day_index]}",
        'Nineveh': nineveh
    }

    for name, offset in offsets.items():
        results[name] = add_days(nineveh, offset)

    return results


if __name__ == "__main__":
    import json
    yearStart = int(input("Enter the starting Ethiopian year: "))
    yearEnd = int(input("Enter the ending Ethiopian year:  "))
    for year in range(yearStart, yearEnd + 1):
        data = compute_fasts_and_feasts(year)
        printable = {k: str(v) for k, v in data.items()}
        print(f"\n--- Year {year} ---")
        print(json.dumps(printable, ensure_ascii=False, indent=2))

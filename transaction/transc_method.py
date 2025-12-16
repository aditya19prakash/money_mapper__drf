import random
import pandas as pd
import numpy as np


class Excel_cleaning:

    @staticmethod
    def convert_integer(value):
        if pd.isna(value):
            return None
        try:
            return int(value)
        except (ValueError, TypeError):
            return None

    @staticmethod
    def convert_text(value):
        if not isinstance(value, str):
            return None
        return value.strip()

    @staticmethod
    def clean(file,user_id) -> list[dict]:
        try:
            df = pd.read_excel(
                file,
                engine="openpyxl",
                skiprows=19
            )

            df = df.iloc[:, :6]
            df.columns = [
                "txn_date",
                "value_date",
                "description",
                "ref_no",
                "debit",
                "credit",
            ]

            df.drop(columns=["ref_no", "value_date"], inplace=True)

           
            df["txn_date"] = pd.to_datetime(
                df["txn_date"],
                format="%d-%m-%Y",
                errors="coerce"
            ).dt.date

            df["user"] = user_id

   
            df["debit"] = (
                pd.to_numeric(df["debit"], errors="coerce")
                .apply(Excel_cleaning.convert_integer)
            )

            df["credit"] = (
                pd.to_numeric(df["credit"], errors="coerce")
                .apply(Excel_cleaning.convert_integer)
            )

          
            df = df[
                df["description"].notna() &
                df["description"].astype(str).str.strip().ne("")
            ]

       
            df["description"] = df["description"].apply(
                Excel_cleaning.convert_text
            )

          
            df = df[~(df["debit"].isna() & df["credit"].isna())]

         
            df["account_name"] = df["description"].apply(
                Excel_cleaning.extract_name
            )

            df["payment_method"] = df["description"].apply(
                Excel_cleaning.extract_payment_method
            )

            df["category"] = df["account_name"]

            df["id"] = df["description"].apply(
                Excel_cleaning.extract_transc_id
            )
            df = df.reset_index(drop=True)
            df = df.replace({np.nan: None})
            return df.to_dict(orient="records")

        except Exception as e:
            return[{
                "error": "Excel processing failed",
                "details": str(e),
            }]

    @staticmethod
    def extract_transc_id(description):
        try:
            if Excel_cleaning.extract_payment_method(description)!="UPI":
                raise ValueError("")
            parts = str(description).split("/")
            if len(parts) > 2:
                return parts[2].strip()
        except:
            return random.randint(100000000000, 999999999999)

    @staticmethod
    def extract_payment_method(description):
        if not isinstance(description, str):
            return "Unknown"

        desc = description.upper()

        data = {
            "CDM SERVICE CHARGES": "Service Charges",
            "UPI": "UPI",
            "CDM": "Money Transfer",
            "CHEQUE": "Cheque",
            "ATM": "ATM",
            "NEFT": "NEFT",
            "IMPS": "IMPS",
        }

        for key, value in data.items():
            if key in desc:
                return value

        return "Unknown"

    @staticmethod
    def extract_name(description):
        if not isinstance(description, str):
            return "Unknown"

        d = description.upper()

        if "DEBIT CARD" in d:
            return "Debit Card"
        if "CREDIT CARD" in d:
            return "Credit Card"

        parts = description.split("/")
        return parts[3].strip() if len(parts) > 3 else "Unknown"

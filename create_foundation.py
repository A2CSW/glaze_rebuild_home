import pandas as pd
import os

os.makedirs('data', exist_ok=True)

# Full student list from your data
full_names = [
"Aaron Henzell-Hill", "Abbie Laing", "Abby Ward", "Abi Dickinson", "Abigail Simpson", "Ada Dolinson", "Ada Rigby", "Adam Hogg", "Adam Williams", "Aidan Morley", "Aiden Forrest", "Aiesha Potts", "Aiva MaCallister", "Alesha Assam", "Alex Evans", "Alexa Terry", "Alexander Perfect", "Alexia-Jo Wood", "Alfie Henderson", "Alfie Hiscocks", "Alfie Jones", "Alfie Sparrowhawk", "Alice Robinson", "Alice Storey", "Alice Wilde", "Alyvia Neder", "Amelia Collins", "Amelia Glascott", "Amelia Shield", "Amelie Bales", "Amelie Carter", "Amie Butler", "Amy Brent", "Amy Johnson", "Anna Rowley", "Anna-Rose Crawford", "Annabelle Hogan", "April James", "Arlo Walker", "Arthur Law", "Asa Mather", "Ash Hope", "Austin Beal", "Ava Borthwick", "Ava Brown", "Ava Harland", "Ava Maylin-Donnell", "Ava Nolan", "Ava Smith", "Beatrix Grant", "Bella Rea", "Bella Similon", "Bella Storey", "Ben Ledger", "Ben O'Hara", "Ben Rowley", "Ben Whiffin", "Bendigedig Willis", "Benjamin Moses", "Bertie Govantes", "Beth Cole", "Beth Richards", "Bethany Aust", "Billie Horrobin", "Bo Reef Davies", "Bobby McGarvie", "Brogan Fine", "Cait Marshall", "Cali Legge", "Calvin Maddison", "Cameron McMorran", "Caradoc Willis", "Casper Thompson Armstrong", "Cassidy Coulter", "Cerys James", "Charlie Ledger", "Charlie Mollett", "Charlie Wood", "Charlotte Ginzel-Forster", "Charlotte Patterson-Jones", "Charlotte Waters", "Charlotte Williams", "Charlotte Wilson", "Chloe Hubbard", "Chloe McNamara Renzo", "Chloe Patterson", "Cohen Mitchell", "Connie Crammond", "Coral Nichol", "Courtney Hopkins", "Daisy Harrop", "Darcey Beattie", "Edith Bovingdon", "Eleanor Kirkup", "Ellie Wardle", "Elyse Alltimes", "Erin & Lois Fordy", "Etta Forrester-Grange", "Eva Gibson", "Finlay Alisandratos", "Georgia Rowley", "Harriet & Lilian Woods", "Harrison Cory", "Heidi Shorting", "Holden Partington", "Ivy Wyatt", "Jack Mason", "Jake Hudson", "Jonty Hall", "Joyce Schannen", "Kit Gresswell-Pettit", "Lily Dixon", "Logan McMahon", "Lucy Blackett", "Lucy Pears", "Lyra Sorbie", "Martha Macleod", "Macey McGwinn", "Maple Garnish", "Neve Hardy", "Oliver Walton", "Poppy Harrison", "Richie Chalder", "Roma Burridge", "Ruby Cairney", "Sam Glancy", "Serenity Cooke", "Sophie Gillone", "Stan McVey", "Sylvie MacKnight", "Teddy Fellows", "Thea Morrison-Cairns", "Zari Idowu-Read"
]

students = pd.DataFrame([name.split(maxsplit=1) for name in full_names], columns=["FirstName", "LastName"])
students["StudentID"] = range(101, 101 + len(students))
students["Status"] = "Current"

students = students[["StudentID", "FirstName", "LastName", "Status"]]
students.to_csv('data/students.csv', index=False)

print(f"✅ Created data/students.csv — **{len(students)} students**")

# References file
references = pd.DataFrame({
    "StudentID": students["StudentID"],
    "StudentName": students["FirstName"] + " " + students["LastName"],
    "ReferencePattern": ""
})
references.to_csv('data/reference_patterns.csv', index=False)

print("✅ Created data/reference_patterns.csv")
print("\nHistorical foundation complete!")

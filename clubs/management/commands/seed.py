from django.core.management.base import BaseCommand
from faker import Faker
import random as random
from clubs.models import User, Club, Role

class Command(BaseCommand):
    def __init__(self):
        super().__init__()
        self.faker = Faker('en_GB')

    def getRandomSkillLevel(self):
        skillList = (
            ("1", "One"),
            ("2", "Two"),
            ("3", "Three"),
            ("4", "Four"),
            ("5", "Five")
            )
        randomNum = random.randint(1,5)
        return skillList[randomNum-1]

    def getRandomStatusLevel(self):
        randomNum = random.randint(1,4)
        if(randomNum % 4 == 0):
            return "Officer"
        else:
            return "Member"

    def handle(self, *args, **options):
        faker_users = []
        faker_clubs = []
        user_amount = 100
        club_amount = 10

        ownerForAll = User.objects.create_user('@ownerAll',
                                        first_name="Admin",
                                        last_name="Owner",
                                        email="ownerForAll@email.com",
                                        password="Password123",
                                        chess_Level= self.getRandomSkillLevel(),
                                        personal_statement=f"The head owner of most chess clubs",
                                        bio=f"The head owner of most chess clubs made.")
        ownerForAll.save()


        kerbal_club = Club.objects.create(
        name = "Kerbal Club",
        location = "Kermin",
        description = "The Official Kermin Chess Club",
        number_of_members = 0
        )
        kerbal_club.save()
        print(f"Added {kerbal_club.name}")

        club_1 = Club.objects.create(
        name = "London Club",
        location = "London",
        description = "The Official London Chess Club",
        number_of_members = 0
        )
        club_1.save()
        print(f"Added {club_1.name}")

        londonOwner = Role.objects.create(
                   user = ownerForAll,
                   club = club_1,
                   club_role = "Owner"
        )
        club_1.number_of_members += 1
        club_1.save()
        print(f"Assigned {ownerForAll.first_name} as owner to ({club_1.name})")



        club_2 = Club.objects.create(
        name = "Barcelona Club",
        location = "Barcelona",
        description = "The Official Barcelona Chess Club",
        number_of_members = 0
        )
        club_2.save()
        print(f"Added {club_2.name}")

        club_3 = Club.objects.create(
        name = "Paris Club",
        location = "Paris",
        description = "The Official Paris Chess Club",
        number_of_members = 0
        )
        club_3.save()
        print(f"Added {club_3.name}")

        parisOwner = Role.objects.create(
                   user = ownerForAll,
                   club = club_3,
                   club_role = "Owner"
        )
        club_3.number_of_members += 1
        club_3.save()
        print(f"Assigned {ownerForAll.first_name} as owner to ({club_3.name})")

        jeb = User.objects.create_user(
        username ="@jeb",
        first_name = "Jebediah",
        last_name = "Kerman",
        email = "jeb@example.org",
        password = "Password123",
        chess_Level = self.getRandomSkillLevel(),
        personal_statement=f"I love chess! My favourite number is: "
                           f"{random.randint(1,100)}.",
        bio= "Hi my name is Jebediah"
        )
        jeb.save()
        jebRole = Role.objects.create(
                     user = jeb,
                     club = kerbal_club,
                     club_role = "Member",
        )
        jebLondonRole = Role.objects.create(
                            user = jeb,
                            club = club_1,
                            club_role = "Officer"
        )
        kerbal_club.number_of_members += 1
        kerbal_club.save()
        club_1.number_of_members += 1
        club_1.save()
        print(f"Added {jeb.username}")

        valentina = User.objects.create_user(
        username ="@valentina",
        first_name = "Valentina",
        last_name = "Kerman",
        email = "val@example.org",
        password = "Password123",
        chess_Level = self.getRandomSkillLevel(),
        personal_statement=f"I love chess! My favourite number is: "
                           f"{random.randint(1,100)}.",
        bio= "Hi my name is Valentina",
        )
        valentina.save()

        valentinaRole = Role.objects.create(
                     user = valentina,
                     club = kerbal_club,
                     club_role = 'Officer'
                     )

        valentinaBarcelonaRole = Role.objects.create(
                            user = valentina,
                            club = club_2,
                            club_role = 'Owner'
                            )


        kerbal_club.number_of_members += 1
        kerbal_club.save()
        club_2.number_of_members += 1
        club_2.save()
        print(f"Added {valentina.username}")


        billie= User.objects.create_user(
        username ="@billie",
        first_name = "Billie",
        last_name = "Kerman",
        email = "billie@example.org",
        password = "Password123",
        chess_Level = self.getRandomSkillLevel(),
        personal_statement=f"I love chess! My favourite number is: "
                           f"{random.randint(1,100)}.",
        bio= "Hi my name is Billie",
        )
        billie.save()
        billieRole = Role.objects.create(
                     user = billie,
                     club = kerbal_club,
                     club_role = "Owner",
        )
        billieParisRole = Role.objects.create(
                            user = billie,
                            club = club_3,
                            club_role = "Member"
        )
        kerbal_club.number_of_members += 1
        kerbal_club.save()
        club_3.number_of_members += 1
        club_3.save()
        print(f"Added {billie.username}")

        #Loop to create 10 random clubs for the users to join
        for i in range(0, club_amount):
            while True:
                club_name = self.faker.country() + " Club"
                club_location = self.faker.city()
                club_description = f"This is the official club of {club_name}."
                if club_name not in faker_clubs:
                    faker_clubs.append(club_name)
                    club = Club.objects.create(
                           name = club_name,
                           location = club_location,
                           description = club_description,
                           )
                    club.save()
                    clubList = list(Club.objects.all())
                    clubNo = clubList[i+4]
                    userRole = Role.objects.create(
                               user = ownerForAll,
                               club = clubNo,
                               club_role = "Owner"
                    )
                    clubNo.number_of_members += 1
                    clubNo.save()
                    print(f"Added {club_name} ({i + 1}/{club_amount})")
                    print(f"Assigned {ownerForAll.first_name} as owner to ({clubNo.name})")
                    break



        #Loop to create 100 random users which also get assigned "roles" when they join a club
        for i in range(0, user_amount):
            while True:
                faker_first_name = self.faker.first_name()
                faker_last_name = self.faker.last_name()
                faker_user_name = "@" + faker_first_name + faker_last_name
                faker_email = faker_first_name.lower() + faker_last_name.lower() + "@" + self.faker.free_email_domain()
                if faker_user_name not in faker_users:
                    faker_users.append(faker_user_name)
                    user = User.objects.create_user(username=faker_user_name,
                                                    first_name=faker_first_name,
                                                    last_name=faker_last_name,
                                                    email=faker_email,
                                                    password="Password123",
                                                    chess_Level= self.getRandomSkillLevel(),
                                                    personal_statement=f"I love chess! My favourite number is: "
                                                                       f"{random.randint(1,100)}.",
                                                    bio=f"Hi my name is {faker_first_name}.")
                    user.save()
                    randomNum = random.randint(0, Club.objects.all().count() - 1)
                    clubList = list(Club.objects.all())
                    randomClub = clubList[randomNum]
                    userRole = Role.objects.create(
                               user = user,
                               club = randomClub,
                               club_role = self.getRandomStatusLevel()
                    )
                    randomClub.number_of_members += 1
                    randomClub.save()
                    print(f"Added {faker_user_name} as { userRole.club_role} ({i + 1}/{user_amount}) to {randomClub.name}")
                    break

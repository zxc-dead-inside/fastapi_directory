import asyncio
import random

from faker import Faker

from app.database import (
    Building,
    Activity,
    Office,
    Organization,
    OrganizationPhone,
    OrganizationActivity,
    OrganizationOffice,
)
from app.database.database import get_database

fake = Faker("ru_RU")
Faker.seed(1)
random.seed(1)


async def seed_buildings(session, count: int = 50) -> list[Building]:
    buildings = [
        Building(
            address=fake.address().replace("\n", ", "),
            lat=fake.latitude(),
            lon=fake.longitude(),
        )
        for _ in range(count)
    ]
    session.add_all(buildings)
    await session.flush()
    print(f"Добавлено {count} зданий.")
    return buildings


async def seed_activities(session) -> list[Activity]:
    root_food = Activity(name="Еда", level=0)
    meat = Activity(name="Мясная продукция", parent=root_food, level=1)
    dairy = Activity(name="Молочная продукция", parent=root_food, level=1)
    cars = Activity(name="Автомобили", level=0)
    trucks = Activity(name="Грузовые", parent=cars, level=1)
    cars_light = Activity(name="Легковые", parent=cars, level=1)
    parts = Activity(name="Запчасти", parent=cars_light, level=2)
    accessories = Activity(name="Аксессуары", parent=cars_light, level=2)

    all_acts = [root_food, meat, dairy, cars, trucks, cars_light, parts, accessories]
    session.add_all(all_acts)
    await session.flush()
    print(f"Добавлено {len(all_acts)} видов деятельности.")
    return all_acts


async def seed_organizations(session, buildings, activities, count: int = 100):
    used_pairs: dict[str, set[tuple[int, str]]] = {}

    organizations: list[Organization] = []

    for _ in range(count):
        org = Organization(name=fake.company())
        organizations.append(org)
    session.add_all(organizations)
    await session.flush()

    phones: list[OrganizationPhone] = []
    for org in organizations:
        for _ in range(random.randint(1, 3)):
            phones.append(
                OrganizationPhone(
                    organization_id=org.id,
                    phone_number=fake.phone_number(),
                )
            )
    session.add_all(phones)

    offices: list[Office] = []
    org_offices: list[OrganizationOffice] = []
    for org in organizations:
        b = random.choice(buildings)
        if b.id not in used_pairs:
            used_pairs[b.id] = set()

        for _ in range(100):
            floor = random.randint(1, 10)
            unit = str(random.randint(1, 20))
            if (floor, unit) not in used_pairs[b.id]:
                used_pairs[b.id].add((floor, unit))
                break
        else:
            raise RuntimeError(
                f"Не удалось подобрать уникальный офис для здания {b.id}")

        office = Office(building_id=b.id, floor=floor, unit=unit)
        offices.append(office)
        session.add(office)
        await session.flush()
        org_offices.append(
            OrganizationOffice(organization_id=org.id, office_id=office.id))

    session.add_all(offices)
    session.add_all(org_offices)

    org_activities: list[OrganizationActivity] = []
    for org in organizations:
        acts = random.sample(activities,
                             random.randint(1, min(3, len(activities))))
        for act in acts:
            org_activities.append(
                OrganizationActivity(organization_id=org.id,
                                     activity_id=act.id)
            )
    session.add_all(org_activities)

    print(f"{len(organizations)} организаций, {len(phones)} телефонов, "
          f"{len(offices)} офисов, {len(org_activities)} связей по видам деятельности.")


async def main():
    db = get_database()
    async with db.session() as session:
        buildings = await seed_buildings(session)
        activities = await seed_activities(session)
        await seed_organizations(session, buildings, activities)
    await db.dispose()


if __name__ == "__main__":
    asyncio.run(main())

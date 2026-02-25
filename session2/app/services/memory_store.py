from domain.models import Meeting

metting = Meeting("id", "title", "date", "owner", ["joao", "diogo"], [{"dsad", "wner", "date"}])
metting2 = Meeting("id", "title", "date", "owner", ["joao", "diogo"], [{"dsad", "wner", "date"}])

meetings: list[Meeting] = [metting, metting2]
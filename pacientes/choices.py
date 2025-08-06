import datetime, pycountry

#Choices

dias = [(str(day).zfill(2), str(day).zfill(2)) for day in range(1, 32)]

meses = (
    ('January', 'January'),
    ('February', 'February'),
    ('March', 'March'),
    ('April', 'April'),
    ('May', 'May'),
    ('June', 'June'),
    ('July', 'July'),
    ('August', 'August'),
    ('September', 'September'),
    ('October', 'October'),
    ('November', 'November'),
    ('December', 'December')
)

current_year = datetime.datetime.now().year
anos = [(str(year), str(year)) for year in range(current_year, 1949, -1)]

paises = sorted(
    [(country.name, country.name) for country in pycountry.countries],
    key=lambda x: x[1]
)

queixas = (
    ('TDAH', 'TDAH'),
    ('DEPRESSÃO', 'Depressão'),
    ('ANSIEDADE', 'Ansiedade'),
    ('TAG', 'Transtorno de Ansiedade Generalizada'),
    ('TOC', 'TOC')
)

frequencia = (
    ('D', 'Diário'),
    ('1S', '1 vez por semana'),
    ('2S', '2 vezes por semana'),
    ('3S', '3 vezes por semana'),
    ('N', 'Ao necessitar')
)

tarefas = (
    ('Meditação', 'Meditação'),
    ('Respiração', 'Respiração'),
    ('Anotação', 'Anotação'),
    ('Medicação', 'Medicação'),
    ('Conversação', 'Conversação')
)
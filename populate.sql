INSERT INTO professionals
    (council_number, name, email, phone, password, specialty, address)
VALUES
    ("1234", "John Doe", "john@mail.com","(99)9999-9999","123456","Psiquiatria","Rua 1, nº 10, Bairro 7, Cidade C"),
    ("1235", "Jane Doe", "jane@mail.com","(99)8888-8888","123456","Psiquiatria","Rua 1, nº 10, Bairro 7, Cidade C"),
    ("4321", "Billy Doe", "billy@mail.com","(99)9777-9999","123456","Pediatria","Rua 8, nº 666, Bairro 1, Cidade C"),
    ("5321", "Joe Doe", "joe@mail.com","(99)9666-9999","123456","Fisiatria","Rua 7, nº 12, Bairro 2, Cidade C"),
    ("1233", "Mary Doe", "mary@mail.com","(99)9555-9999","123456","Otorrinolaringologia","Rua 13, nº 52, Bairro 4, Cidade C"),
    ("3321", "Nancy Doe", "nancy@mail.com","(99)9444-9999","123456","Oftalmologia","Rua 11, nº 26, Bairro 6, Cidade C"),
    ("1020", "Claire Doe", "claire@mail.com","(99)9333-9999","123456","Neurologia","Rua 5, nº 32, Bairro 5, Cidade C"),
    ("8512", "Tom Doe", "tom@mail.com","(99)9222-9999","123456","Nefrologia","Rua 56, nº 1753, Bairro 9, Cidade C"),
    ("5952", "Karen Doe", "karen@mail.com","(99)9111-9999","123456","Urologia","Rua 22, nº 1, Bairro 12, Cidade C"),
    ("6542", "Dave Doe", "dave@mail.com","(99)9000-9999","123456","Pneumologia","Rua 34, nº 1325, Bairro 10, Cidade C");

INSERT INTO patients
    (cpf, name, age ,gender , email, password , phone , health_insurance)
VALUES
    ('01002003040', 22, "Julia", "Feminino", "julia@mail.com","12345","(55)5555-5555","Plano A" ),
    ('02003004050', 90, "Maria", "Feminino", "maria@mail.com","12345","(55)4444-5555","Plano Z" ),
    ('03004005060', 53, "João", "Masculino", "jao@mail.com","12345","(55)3333-5555","Plano A" ),
    ('04005006070', 18, "Marcos", "Masculino", "markin@mail.com","12345","(55)5222-5555","Plano D" ),
    ('05006007080', 38, "Raul", "Masculino", "raul@mail.com","12345","(55)51111-5555","Plano B" ),
    ('06007008090', 44, "Mira", "Feminino", "mira@mail.com","12345","(55)5554-5555","Plano A" ),
    ('07008009000', 2021, "Jesus", "Masculino", "jesus@mail.com","12345","(55)6555-5555","Plano V" ),
    ('0800900010', 20, "Alice", "Feminino", "julia@mail.com","12345","(55)9555-5555","Plano A" ),

INSERT INTO appointments
    (professional_id , pacient_id , date, finished )
VALUES
    ('1234', '01002003040', "2021-12-31", False),
    ('1234', '01002003040', "2018-01-31", True),
    ('1234', '01002003040', "2022-01-31", False),
    ('1234', '01002003040', "2022-02-10", False),
    ('1234', '01002003040', "2021-06-25", True),
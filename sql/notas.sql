CREATE TABLE aluno (
  	matricula CHAR(5) NOT NULL,  
  	nome VARCHAR(80) NOT NULL,
  	dt_nasc DATE NOT NULL,
   PRIMARY KEY(matricula));
   
CREATE TABLE nota(
   	id int unsigned NOT null  AUTO_INCREMENT,
     disciplina VARCHAR(50) NOT NULL,
     av1 float,
     av2 float,
     matricula char(5) NOT NULL,
   PRIMARY KEY(id));
   
INSERT INTO aluno(matricula, nome, dt_nasc)
VALUES (12345, 'Iago', '2006-05-17'),
(81928, 'Roberto', '2006-08-08');
SELECT * from aluno

#Atualizar tabelas
UPDATE aluno
SET matricula = 16733
WHERE matricula = 12345;

#Apagar tabelas
delete from aluno
where matricula = 81928
LIMIT 1;

#Consultar tabelas
SELECT matricula, nome
FROM aluno
ORDER BY nome;
   
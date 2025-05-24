--Classe Pessoa
local Pessoa = {}
Pessoa.__index = Pessoa

function Pessoa.new(nome, idade)
  local self = setmetatable({}, Pessoa)
  self.nome  = nome
  self.idade = idade
  return self
end

function Pessoa:apresentar()
  print("Olá, eu sou " .. self.nome .. ", tenho " .. self.idade .. " anos.")
end

-- Uso
local p = Pessoa.new("Ana", 30)
p:apresentar()

-- Classe Aluno herda de Pessoa
local Aluno = setmetatable({}, { __index = Pessoa })
Aluno.__index = Aluno

function Aluno.new(nome, idade, curso)
  local self = Pessoa.new(nome, idade)
  setmetatable(self, Aluno)
  self.curso = curso
  return self
end

function Aluno:estudar()
  print(self.nome .. " está estudando " .. self.curso)
end

-- Uso
local a = Aluno.new("Bruno", 22, "Engenharia")
a:apresentar()  -- método herdado
a:estudar()      -- próprio

-- Campos privados via escopo
local Conta = {}
Conta.__index = Conta

function Conta.new(saldo_inicial)
  local saldo = saldo_inicial  -- variável local “privada”
  local self = setmetatable({}, Conta)
  function self:depositar(v) saldo = saldo + v end
  function self:ver_saldo() print("Saldo:", saldo) end
  return self
end

-- Uso
local c = Conta.new(100)
c:depositar(50)
c:ver_saldo()  -- não acessa saldo diretamente

--Metatable
local t = {}
setmetatable(t, {
  __index = function(tbl, key)
    return "chave '"..key.."' não definida"
  end,
  __newindex = function(tbl, key, val)
    print("Definindo", key, "=", val)
    rawset(tbl, key, val)  -- evita loop
  end
})

print(t.foo)   -- “chave 'foo' não definida”
t.bar = 10     -- imprime “Definindo bar = 10”
print(t.bar)   -- 10

-- tostring
local mt = {
    __tostring = function(self)
      return "["..self.x..","..self.y.."]"
    end
  }
local v = setmetatable({x=3, y=4}, mt)
print(v)       -- “[3,4]”

-- add
mt.__add = function(a,b)
  return setmetatable({ x=a.x+b.x, y=a.y+b.y }, mt)
end
local u = {x=1, y=2}
setmetatable(u, mt)
print((u + v)) -- “[4,6]”

-- call
mt.__call = function(self, a,b)
  return { x=self.x+a, y=self.y+b }
end
setmetatable(v, mt)
local w = v(5,6)
print(w.x, w.y) -- 8 10

-- “Classe” básica
local Base = {}
Base.__index = Base
function Base:greet() print("Oi!") end

-- “Subclasse” simplesmente usa __index para cadeia
local Sub = {}
setmetatable(Sub, { __index = Base })
Sub.__index = Sub

function Sub:new()
  return setmetatable({}, Sub)
end

local obj = Sub:new()
obj:greet()  -- busca em Sub, depois em Base


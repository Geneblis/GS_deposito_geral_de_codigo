#include <stdio.h>
#include <lua.h>
#include <lualib.h>
#include <lauxlib.h>

int main() {
    lua_State *L = luaL_newstate();      // Cria a máquina virtual Lua
    luaL_openlibs(L);                    // Carrega as bibliotecas padrão do Lua

    // Executa o script Lua
    if (luaL_dofile(L, "quiz.lua") != LUA_OK) {
        fprintf(stderr, "Erro ao executar Lua: %s\n", lua_tostring(L, -1));
        lua_close(L);
        return 1;
    }

    lua_close(L); // Fecha a VM do Lua
    return 0;
}

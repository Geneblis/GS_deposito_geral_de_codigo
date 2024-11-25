package com.blackbird.game;

import com.badlogic.gdx.graphics.Texture;
import com.badlogic.gdx.graphics.g2d.Sprite;
import com.badlogic.gdx.graphics.g2d.SpriteBatch;

public class Bala {
    private float x;
    private float y;
    private final float angle;
    private final float size;
    private final float speed;
    private final Texture blackbirdTexture;
    private final Sprite blackbirdSprite;

    // Construtor da bala
    public Bala(float x, float y, float angle, float size, float speed) {
        this.x = x;
        this.y = y;
        this.angle = angle;
        this.size = size;
        this.speed = speed;
        blackbirdTexture = new Texture("blackbird.png");
        blackbirdSprite = new Sprite(blackbirdTexture);
        blackbirdSprite.setSize(size, size);
        blackbirdSprite.setOrigin(size / 2, size / 2); //Dividir o tamamho por 2 coloca a origem para o centro.
        blackbirdSprite.setRotation(angle);
    }

    //Para definir o metodo atirar foi necessario chamar a Classe player, variavel X, varivel Y, variavel angle, offset definido em Main, size e speed tb.
    public static Bala atirar(float playerX, float playerY, float angle, float offset, float size, float speed) {
        float posicao_da_bala_X = playerX + (float) Math.cos(Math.toRadians(angle)) * offset;
        float posicao_da_bala_Y = playerY + (float) Math.sin(Math.toRadians(angle)) * offset;
        return new Bala(posicao_da_bala_X, posicao_da_bala_Y, angle, size, speed);
    }

    public void update() {
        x += Math.cos(Math.toRadians(angle)) * speed;
        y += Math.sin(Math.toRadians(angle)) * speed;
        blackbirdSprite.setPosition(x, y); // Atualiza a posição da sprite
    }

    public void draw(SpriteBatch batch) {
        blackbirdSprite.draw(batch); // Desenha a sprite da bala
    }

    public boolean check(float width, float height) {
        return x >= 0 && x <= width && y >= 0 && y <= height; // Verifica se a bala está dentro da tela
    }

    public void dispose() {
        blackbirdTexture.dispose(); // Libera a textura da bala
    }
}
package com.blackbird.game;

import com.badlogic.gdx.graphics.Texture;
import com.badlogic.gdx.graphics.g2d.Sprite;
import com.badlogic.gdx.graphics.g2d.SpriteBatch;

public class Bala {
    private float x;
    private float y;
    private final float angle;
    private final float size;
    private float speed;
    private Texture blackbirdTexture;
    private Sprite blackbirdSprite;

    public Bala(float x, float y, float angle, float size, float speed) {
        this.x = x;
        this.y = y;
        this.angle = angle;
        this.size = size;
        this.speed = speed;
        blackbirdTexture = new Texture("blackbird.png");
        blackbirdSprite = new Sprite(blackbirdTexture);
        blackbirdSprite.setSize(size, size);
        blackbirdSprite.setOrigin(size / 2, size / 2);
        blackbirdSprite.setRotation(angle);
    }

    public void update() {
        x += Math.cos(Math.toRadians(angle)) * speed;
        y += Math.sin(Math.toRadians(angle)) * speed;
        blackbirdSprite.setPosition(x, y);
    }

    public void draw(SpriteBatch batch) {
        blackbirdSprite.draw(batch);
    }

    // Verifica se a bala está dentro da tela
    public boolean check(float width, float height) {
        return x >= 0 && x <= width && y >= 0 && y <= height;
    }

    public void dispose() {
        blackbirdTexture.dispose();
    }
}
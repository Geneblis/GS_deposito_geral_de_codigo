package com.blackbird.game;

import com.badlogic.gdx.Gdx;
import com.badlogic.gdx.graphics.Texture;
import com.badlogic.gdx.graphics.g2d.Sprite;
import com.badlogic.gdx.graphics.g2d.SpriteBatch;
import com.badlogic.gdx.math.Vector2;

public class Player {

    private SpriteBatch batch;
    public static final float PLAYER_SIZE = 64;
    private Vector2 position;
    private float angle = 0f;
    private Texture playerImage;
    private Texture playerImageSpeed;
    private Sprite playerSprite;

    //velocidade e aceleracao
    private float max_speed =4f;
    private float speed=1f;
    private float aceleracao = 0.2f;
    private float desaceleracao = 0.2f;
    public boolean speedUp = false;

    public Player() {
        playerImage = new Texture("plane.png");
        playerImageSpeed = new Texture("plane_speed.png");
        playerSprite = new Sprite(playerImage);
        position = new Vector2();
        playerSprite.setOrigin(playerSprite.getWidth() / 2, playerSprite.getHeight() / 2); //Dividir o tamamho por 2 coloca a origem para o centro.
    }

    public void changeAngle(float angle) {
        if (angle < 0) {
            angle = 359;
        } else if (angle > 359) {
            angle = 0;
        }
        this.angle = angle;
    }

    public void setAngle(float angle) {
        this.angle = angle;
    }

    public void checkSpeed(){
        if(speedUp == false){
            playerSprite.setTexture(playerImage);
        } else {
            playerSprite.setTexture(playerImageSpeed);
        }
    }

    public void draw(SpriteBatch batch) {
        playerSprite.setPosition(position.x, position.y);
        playerSprite.setRotation(angle);
        playerSprite.draw(batch);
    }

    public void definirPosicao(float x, float y) {
        position.set(x, y);
    }

    public float getX() {
        return position.x;
    }

    public float getY() {
        return position.y;
    }

    public float getAngle() {
        return angle;
    }

    public void update() {
        position.x += Math.cos(Math.toRadians(angle)) * speed;
        position.y += Math.sin(Math.toRadians(angle)) * speed;
    }

    public void accelerate() {
        if (speed < max_speed) { //velocidade atual tem q ser menor que a maxima.
            speed += aceleracao;
            if (speed > max_speed) {
                speed = max_speed;
            }
        }
    }
    public void decelerate() {
        if (speed > 0) {
            speed -= desaceleracao;
            if (speed < 0) {
                speed = 0;
                speedUp=false;
                checkSpeed();
                //caso estiver parado, checar sprite.
            }
        }
    }

    public void dispose() {
        playerImage.dispose();
        playerImageSpeed.dispose();
    }
}
package com.nikitomiamor.classicrabbits;

import java.util.List;

/**
 * Ajustes de las animaciones de 26.3 para el modelo clasico.
 * Archivo generado por rabbit_spec.py: no editar a mano.
 */
public final class ClassicRabbitAdaptRules {
    private ClassicRabbitAdaptRules() {}

    /** Canal (animacion, hueso, tipo) que se reasigna a otro hueso con un factor. */
    public record Rule(String animation, String bone, String target, String newBone, float factor) {}

    public static final List<Rule> RULES = List.of(
        new Rule("HOP", "backlegs", "ROTATION", "left_haunch", 0.25F),
        new Rule("HOP", "backlegs", "ROTATION", "right_haunch", 0.25F),
        new Rule("IDLE_HEAD_TILT", "head", "POSITION", "head", 0.0F),
        new Rule("BABY_HOP", "backlegs", "ROTATION", "left_haunch", 0.25F),
        new Rule("BABY_HOP", "backlegs", "ROTATION", "right_haunch", 0.25F),
        new Rule("BABY_IDLE_HEAD_TILT", "head", "POSITION", "head", 0.0F)
    );
}

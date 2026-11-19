package com.nikitomiamor.classicrabbits;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import net.minecraft.client.animation.AnimationChannel;
import net.minecraft.client.animation.AnimationDefinition;
import net.minecraft.client.animation.Keyframe;
import net.minecraft.client.animation.definitions.BabyRabbitAnimation;
import net.minecraft.client.animation.definitions.RabbitAnimation;
import org.joml.Vector3f;

/**
 * Takes the 26.3 animations and applies the rules from {@link ClassicRabbitAdaptRules}:
 * a channel can be moved to another bone and scaled. Everything else stays the same.
 */
public final class ClassicRabbitAnimations {
    private ClassicRabbitAnimations() {}

    private static final Map<AnimationDefinition, AnimationDefinition> CACHE = new HashMap<>();

    public static synchronized AnimationDefinition adapt(AnimationDefinition definition) {
        return CACHE.computeIfAbsent(definition, ClassicRabbitAnimations::build);
    }

    private static String nameOf(AnimationDefinition definition) {
        if (definition == RabbitAnimation.HOP) return "HOP";
        if (definition == RabbitAnimation.IDLE_HEAD_TILT) return "IDLE_HEAD_TILT";
        if (definition == BabyRabbitAnimation.HOP) return "BABY_HOP";
        if (definition == BabyRabbitAnimation.IDLE_HEAD_TILT) return "BABY_IDLE_HEAD_TILT";
        return null;
    }

    private static String targetName(AnimationChannel.Target target) {
        if (target == AnimationChannel.Targets.ROTATION) return "ROTATION";
        if (target == AnimationChannel.Targets.POSITION) return "POSITION";
        if (target == AnimationChannel.Targets.SCALE) return "SCALE";
        return "";
    }

    private static AnimationDefinition build(AnimationDefinition definition) {
        String animation = nameOf(definition);
        if (animation == null) {
            return definition;
        }
        Map<String, List<AnimationChannel>> bones = new HashMap<>();
        definition.boneAnimations().forEach((bone, channels) -> {
            for (AnimationChannel channel : channels) {
                String target = targetName(channel.target());
                boolean moved = false;
                for (ClassicRabbitAdaptRules.Rule rule : ClassicRabbitAdaptRules.RULES) {
                    if (rule.animation().equals(animation) && rule.bone().equals(bone) && rule.target().equals(target)) {
                        bones.computeIfAbsent(rule.newBone(), k -> new ArrayList<>()).add(scaled(channel, rule.factor()));
                        moved = true;
                    }
                }
                if (!moved) {
                    bones.computeIfAbsent(bone, k -> new ArrayList<>()).add(channel);
                }
            }
        });
        return new AnimationDefinition(definition.lengthInSeconds(), definition.looping(), bones);
    }

    private static AnimationChannel scaled(AnimationChannel channel, float factor) {
        Keyframe[] in = channel.keyframes();
        Keyframe[] out = new Keyframe[in.length];
        for (int i = 0; i < in.length; i++) {
            Keyframe k = in[i];
            out[i] = new Keyframe(
                k.timestamp(),
                new Vector3f(k.preTarget()).mul(factor),
                new Vector3f(k.postTarget()).mul(factor),
                k.interpolation()
            );
        }
        return new AnimationChannel(channel.target(), out);
    }
}

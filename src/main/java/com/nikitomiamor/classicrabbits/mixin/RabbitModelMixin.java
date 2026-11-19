package com.nikitomiamor.classicrabbits.mixin;

import com.nikitomiamor.classicrabbits.ClassicRabbitAnimations;
import net.minecraft.client.animation.AnimationDefinition;
import net.minecraft.client.animation.KeyframeAnimation;
import net.minecraft.client.model.animal.rabbit.AdultRabbitModel;
import net.minecraft.client.model.animal.rabbit.BabyRabbitModel;
import net.minecraft.client.model.animal.rabbit.RabbitModel;
import net.minecraft.client.model.geom.ModelPart;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Redirect;

/** Al armar las animaciones del conejo (adulto y bebe), usa la version adaptada al modelo clasico. */
@Mixin(RabbitModel.class)
public abstract class RabbitModelMixin {
    @Redirect(
        method = "<init>",
        at = @At(
            value = "INVOKE",
            target = "Lnet/minecraft/client/animation/AnimationDefinition;bake(Lnet/minecraft/client/model/geom/ModelPart;)Lnet/minecraft/client/animation/KeyframeAnimation;"
        ),
        require = 2
    )
    private KeyframeAnimation classicRabbits$bake(AnimationDefinition definition, ModelPart root) {
        if ((Object) this instanceof AdultRabbitModel || (Object) this instanceof BabyRabbitModel) {
            definition = ClassicRabbitAnimations.adapt(definition);
        }
        return definition.bake(root);
    }
}

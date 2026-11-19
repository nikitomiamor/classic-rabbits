package com.nikitomiamor.classicrabbits.mixin;

import com.nikitomiamor.classicrabbits.ClassicBabyRabbitModel;
import net.minecraft.client.model.animal.rabbit.BabyRabbitModel;
import net.minecraft.client.model.geom.builders.LayerDefinition;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfoReturnable;

/** The baby rabbit uses the model made in Blockbench from the 1.12.2 baby. */
@Mixin(BabyRabbitModel.class)
public abstract class BabyRabbitModelMixin {
    @Inject(method = "createBodyLayer", at = @At("HEAD"), cancellable = true)
    private static void classicRabbits$createBodyLayer(CallbackInfoReturnable<LayerDefinition> cir) {
        cir.setReturnValue(ClassicBabyRabbitModel.createBodyLayer());
    }
}

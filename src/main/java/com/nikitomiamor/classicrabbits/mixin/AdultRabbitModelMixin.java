package com.nikitomiamor.classicrabbits.mixin;

import com.nikitomiamor.classicrabbits.ClassicRabbitModel;
import net.minecraft.client.model.animal.rabbit.AdultRabbitModel;
import net.minecraft.client.model.geom.builders.LayerDefinition;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfoReturnable;

/** The adult rabbit uses the 1.12.2 geometry instead of the 26.3 one. */
@Mixin(AdultRabbitModel.class)
public abstract class AdultRabbitModelMixin {
    @Inject(method = "createBodyLayer", at = @At("HEAD"), cancellable = true)
    private static void classicRabbits$createBodyLayer(CallbackInfoReturnable<LayerDefinition> cir) {
        cir.setReturnValue(ClassicRabbitModel.createBodyLayer());
    }
}

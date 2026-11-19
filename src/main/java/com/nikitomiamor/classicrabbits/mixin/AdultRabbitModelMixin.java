package com.nikitomiamor.classicrabbits.mixin;

import com.nikitomiamor.classicrabbits.ClassicRabbitModel;
import net.minecraft.client.model.animal.rabbit.AdultRabbitModel;
import net.minecraft.client.model.geom.builders.LayerDefinition;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfoReturnable;

/** El conejo adulto usa la geometria de 1.12.2 en lugar de la de 26.3. */
@Mixin(AdultRabbitModel.class)
public abstract class AdultRabbitModelMixin {
    @Inject(method = "createBodyLayer", at = @At("HEAD"), cancellable = true)
    private static void classicRabbits$createBodyLayer(CallbackInfoReturnable<LayerDefinition> cir) {
        cir.setReturnValue(ClassicRabbitModel.createBodyLayer());
    }
}

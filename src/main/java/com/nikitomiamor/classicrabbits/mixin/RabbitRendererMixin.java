package com.nikitomiamor.classicrabbits.mixin;

import com.nikitomiamor.classicrabbits.ClassicRabbitTextures;
import net.minecraft.client.renderer.entity.RabbitRenderer;
import net.minecraft.client.renderer.entity.state.RabbitRenderState;
import net.minecraft.resources.Identifier;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfoReturnable;

/** Adulto y bebe usan las texturas clasicas (64x32), como en 1.12.2. */
@Mixin(RabbitRenderer.class)
public abstract class RabbitRendererMixin {
    @Inject(
        method = "getTextureLocation(Lnet/minecraft/client/renderer/entity/state/RabbitRenderState;)Lnet/minecraft/resources/Identifier;",
        at = @At("HEAD"),
        cancellable = true
    )
    private void classicRabbits$texture(RabbitRenderState state, CallbackInfoReturnable<Identifier> cir) {
        cir.setReturnValue(ClassicRabbitTextures.forState(state));
    }
}

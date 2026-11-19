package com.nikitomiamor.classicrabbits;

import java.util.EnumMap;
import java.util.Map;
import net.minecraft.client.renderer.entity.state.RabbitRenderState;
import net.minecraft.resources.Identifier;
import net.minecraft.world.entity.animal.rabbit.Rabbit;

/**
 * Texturas clasicas (layout de 1.12.2). Viven en assets/classic_rabbits/textures/entity/rabbit/,
 * asi un resource pack puede reemplazarlas con el mismo nombre.
 */
public final class ClassicRabbitTextures {
    private ClassicRabbitTextures() {}

    // Adultos: texturas de 1.12.2 tal cual. Bebes: rabbit/baby/, con los ojos 1 px mas abajo.
    private static final Identifier TOAST = tex("", "toast");
    private static final Identifier BABY_TOAST = tex("baby/", "toast");
    private static final Map<Rabbit.Variant, Identifier> ADULT = byVariant("");
    private static final Map<Rabbit.Variant, Identifier> BABY = byVariant("baby/");

    private static Map<Rabbit.Variant, Identifier> byVariant(String dir) {
        Map<Rabbit.Variant, Identifier> map = new EnumMap<>(Rabbit.Variant.class);
        map.put(Rabbit.Variant.BROWN, tex(dir, "brown"));
        map.put(Rabbit.Variant.WHITE, tex(dir, "white"));
        map.put(Rabbit.Variant.BLACK, tex(dir, "black"));
        map.put(Rabbit.Variant.WHITE_SPLOTCHED, tex(dir, "white_splotched"));
        map.put(Rabbit.Variant.GOLD, tex(dir, "gold"));
        map.put(Rabbit.Variant.SALT, tex(dir, "salt"));
        map.put(Rabbit.Variant.EVIL, tex(dir, "caerbannog"));
        return map;
    }

    private static Identifier tex(String dir, String name) {
        return Identifier.fromNamespaceAndPath("classic_rabbits", "textures/entity/rabbit/" + dir + name + ".png");
    }

    public static Identifier forState(RabbitRenderState state) {
        if (state.isToast) {
            return state.isBaby ? BABY_TOAST : TOAST;
        }
        Map<Rabbit.Variant, Identifier> map = state.isBaby ? BABY : ADULT;
        return map.getOrDefault(state.variant, map.get(Rabbit.Variant.BROWN));
    }
}

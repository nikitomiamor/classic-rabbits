package com.nikitomiamor.classicrabbits;

import net.minecraft.client.model.geom.PartPose;
import net.minecraft.client.model.geom.builders.CubeListBuilder;
import net.minecraft.client.model.geom.builders.LayerDefinition;
import net.minecraft.client.model.geom.builders.MeshDefinition;
import net.minecraft.client.model.geom.builders.MeshTransformer;
import net.minecraft.client.model.geom.builders.PartDefinition;

/**
 * Conejo de 1.12.2 armado con los mismos nombres de partes que el conejo de 26.3,
 * para que las animaciones de 26.3 (salto y pararse en dos patas) se le apliquen.
 * Archivo generado por rabbit_spec.py: no editar a mano.
 */
@SuppressWarnings("unused")
public final class ClassicRabbitModel {
    private ClassicRabbitModel() {}

    /** 1.12.2 dibujaba al conejo adulto al 60 %. */
    public static final float SCALE = 0.6F;

    public static LayerDefinition createBodyLayer() {
        MeshDefinition mesh = new MeshDefinition();
        PartDefinition root = mesh.getRoot();
        PartDefinition p_body = root.addOrReplaceChild("body", CubeListBuilder.create(), PartPose.offsetAndRotation(0.0F, 22.0F, 6.0F, 0.0F, 0.0F, 0.0F));
            PartDefinition p_torso = p_body.addOrReplaceChild("torso", CubeListBuilder.create().mirror().texOffs(0, 0).addBox(-3.0F, -2.0F, -10.0F, 6.0F, 5.0F, 10.0F), PartPose.offsetAndRotation(0.0F, -3.0F, 2.0F, -0.349066F, 0.0F, 0.0F));
            PartDefinition p_tail = p_body.addOrReplaceChild("tail", CubeListBuilder.create().mirror().texOffs(52, 6).addBox(-1.5F, -1.5F, 0.0F, 3.0F, 3.0F, 2.0F), PartPose.offsetAndRotation(0.0F, -2.0F, 1.0F, -0.349066F, 0.0F, 0.0F));
            PartDefinition p_head = p_body.addOrReplaceChild("head", CubeListBuilder.create().mirror().texOffs(32, 0).addBox(-2.5F, -4.0F, -5.0F, 5.0F, 4.0F, 5.0F).texOffs(32, 9).addBox(-0.5F, -2.5F, -5.5F, 1.0F, 1.0F, 1.0F), PartPose.offsetAndRotation(0.0F, -6.0F, -7.0F, 0.0F, 0.0F, 0.0F));
                PartDefinition p_left_ear = p_head.addOrReplaceChild("left_ear", CubeListBuilder.create().mirror().texOffs(58, 0).addBox(-1.0F, -5.0F, -0.5F, 2.0F, 5.0F, 1.0F), PartPose.offsetAndRotation(1.3195F, -4.0F, -0.8712F, 0.0F, 0.261799F, 0.0F));
                PartDefinition p_right_ear = p_head.addOrReplaceChild("right_ear", CubeListBuilder.create().mirror().texOffs(52, 0).addBox(-1.0F, -5.0F, -0.5F, 2.0F, 5.0F, 1.0F), PartPose.offsetAndRotation(-1.3195F, -4.0F, -0.8712F, 0.0F, -0.261799F, 0.0F));
            PartDefinition p_frontlegs = p_body.addOrReplaceChild("frontlegs", CubeListBuilder.create(), PartPose.offsetAndRotation(0.0F, -5.0F, -7.0F, 0.0F, 0.0F, 0.0F));
                PartDefinition p_right_front_leg = p_frontlegs.addOrReplaceChild("right_front_leg", CubeListBuilder.create().mirror().texOffs(0, 15).addBox(-1.0F, 0.0F, -1.0F, 2.0F, 7.0F, 2.0F), PartPose.offsetAndRotation(-3.0F, 0.0F, 0.0F, -0.174533F, 0.0F, 0.0F));
                PartDefinition p_left_front_leg = p_frontlegs.addOrReplaceChild("left_front_leg", CubeListBuilder.create().mirror().texOffs(8, 15).addBox(-1.0F, 0.0F, -1.0F, 2.0F, 7.0F, 2.0F), PartPose.offsetAndRotation(3.0F, 0.0F, 0.0F, -0.174533F, 0.0F, 0.0F));
        PartDefinition p_backlegs = root.addOrReplaceChild("backlegs", CubeListBuilder.create(), PartPose.offsetAndRotation(0.0F, 17.5F, 3.7F, 0.0F, 0.0F, 0.0F));
            PartDefinition p_right_hind_leg = p_backlegs.addOrReplaceChild("right_hind_leg", CubeListBuilder.create().mirror().texOffs(16, 15).addBox(-1.0F, 0.0F, 0.0F, 2.0F, 4.0F, 5.0F), PartPose.offsetAndRotation(-3.0F, 0.0F, 0.0F, -0.349066F, 0.0F, 0.0F));
                PartDefinition p_right_haunch = p_right_hind_leg.addOrReplaceChild("right_haunch", CubeListBuilder.create().mirror().texOffs(8, 24).addBox(-1.0F, 5.5F, -3.7F, 2.0F, 1.0F, 7.0F), PartPose.offsetAndRotation(0.0F, 0.0F, 0.0F, 0.349066F, 0.0F, 0.0F));
            PartDefinition p_left_hind_leg = p_backlegs.addOrReplaceChild("left_hind_leg", CubeListBuilder.create().mirror().texOffs(30, 15).addBox(-1.0F, 0.0F, 0.0F, 2.0F, 4.0F, 5.0F), PartPose.offsetAndRotation(3.0F, 0.0F, 0.0F, -0.349066F, 0.0F, 0.0F));
                PartDefinition p_left_haunch = p_left_hind_leg.addOrReplaceChild("left_haunch", CubeListBuilder.create().mirror().texOffs(26, 24).addBox(-1.0F, 5.5F, -3.7F, 2.0F, 1.0F, 7.0F), PartPose.offsetAndRotation(0.0F, 0.0F, 0.0F, 0.349066F, 0.0F, 0.0F));
        return LayerDefinition.create(mesh, 64, 32).apply(MeshTransformer.scaling(SCALE));
    }
}

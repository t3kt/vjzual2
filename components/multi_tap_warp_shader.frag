uniform vec4 tapDisplaceWeightXA;
uniform vec4 tapDisplaceWeightXB;
uniform vec4 tapDisplaceWeightYA;
uniform vec4 tapDisplaceWeightYB;
uniform int horzSource;
uniform int vertSource;
//uniform vec2 sourceMidpoint;

#define SOURCE_NONE 0
#define SOURCE_RED 1
#define SOURCE_GREEN 2
#define SOURCE_BLUE 3
#define SOURCE_ALPHA 4
#define SOURCE_LUMINANCE 5

float getSourceVal(vec4 sourceColor, int sourceType) {
    if (sourceType >= SOURCE_RED && sourceType <= SOURCE_ALPHA) {
        return sourceColor[sourceType - SOURCE_RED];
    }
    if (sourceType == SOURCE_LUMINANCE) {
        return czm_luminance(sourceColor.rgb);
    }
    return 0.0;
}

vec2 getTapOffset(vec2 displaceWeight) {
    vec4 sourceColor = texture(sTD2DInputs[1], vUV.st);
    vec2 offset = vec2(0.0);
    if (horzSource > SOURCE_NONE && horzSource <= SOURCE_LUMINANCE) {
        offset.x = map(getSourceVal(sourceColor, horzSource), 0.0, 1.0, -displaceWeight.x, displaceWeight.x);
    }
    if (vertSource > SOURCE_NONE && vertSource <= SOURCE_LUMINANCE) {
        offset.y = map(getSourceVal(sourceColor, vertSource), 0.0, 1.0, -displaceWeight.y, displaceWeight.y);
    }
    return offset;
}

vec4 getWarpTap(vec2 displaceWeight) {
    vec2 offset = getTapOffset(displaceWeight);
    vec2 uv = vUV.xy + offset;
    return texture(sTD2DInputs[0], uv);
}

vec4 getTapA(int i) {
    return getWarpTap(vec2(tapDisplaceWeightXA[i], tapDisplaceWeightYA[i]));
}
vec4 getTapB(int i) {
    return getWarpTap(vec2(tapDisplaceWeightXB[i], tapDisplaceWeightYB[i]));
}
vec4 getZeroTap() {
    return texture(sTD2DInputs[0], vUV.st);
}

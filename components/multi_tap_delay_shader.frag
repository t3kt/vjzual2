uniform vec4 tapLengthA;
uniform vec4 tapLengthB;

#define W_OFFSET uTD3DInfos[0].depth.z

vec4 getDelayTap(float length, float alpha) {
	return texture(sTD3DInputs[0], vec3(vUV.st, length + W_OFFSET)) * vec4(1.0, 1.0, 1.0, alpha);
}

vec4 getTapA(int i) {
    return getDelayTap(tapLengthA[i], tapAlphaA[i]);
}

vec4 getTapB(int i) {
    return getDelayTap(tapLengthB[i], tapAlphaB[i]);
}

vec4 getZeroTap() {
    return texture(sTD3DInputs[0], vec3(vUV.st, W_OFFSET));
}

layout(location = 0) out vec4 fragColor;
uniform vec2 center;
uniform int samples;
uniform float strength; 
uniform int maskChan;
uniform int maskOn;
uniform vec4 maskRange;
uniform vec2 sampleRange;

// ['luminance', 'red', 'green', 'blue', 'alpha', 'rgbaverage', 'average']
#define MASK_LUMINANCE 0
#define MASK_R 1
#define MASK_G 2
#define MASK_B 3
#define MASK_A 4
#define MASK_RGBAVG 5
#define MASK_RGBAAVG 6

float extractMaskVal(vec4 maskColor)
{
	if (maskChan == MASK_LUMINANCE) {
		return czm_luminance(maskColor.rgb);
	} else if (maskChan == MASK_R) {
		return maskColor.r;
	} else if (maskChan == MASK_G) {
		return maskColor.g;
	} else if (maskChan == MASK_B) {
		return maskColor.b;
	} else if (maskChan == MASK_A) {
		return maskColor.a;
	} else if (maskChan == MASK_RGBAVG) {
		return (maskColor.r + maskColor.g + maskColor.b) / 3.0;
	} else if (maskChan == MASK_RGBAAVG) {
		return (maskColor.r + maskColor.g + maskColor.b + maskColor.a) / 4.0;
	} else {
		return 1.0;
	}
}

float getStrength() {
	float str = strength;
	if (maskOn == 0) {
		return str;
	}
	vec4 maskColor = texture(sTD2DInputs[1], vUV.st);
	float maskVal = extractMaskVal(maskColor);
	return map(maskVal, maskRange.r, maskRange.g, maskRange.b, maskRange.a);
}

void main(void)
{

	vec2 res = uTD2DInfos[0].res.zw;
	vec2 pos = center * res;
	vec2 dir = (gl_FragCoord.xy-pos)/res;
	
	float actualStrength = getStrength();

	vec4 color = vec4(0.0,0.0,0.0,0.0);
	   
	for (int i = 0; i < samples; i += 2) //operating at 2 samples for better performance
	{
		//float sampleStrength = actualStrength * (map(float(samples-i), 0.0, float(samples), sampleRange.x, sampleRange.y));
		float sampleStrength = actualStrength;
		color += texture(sTD2DInputs[0],vUV.st+float(i)/float(samples)*dir*-sampleStrength);
		color += texture(sTD2DInputs[0],vUV.st+float(i+1)/float(samples)*dir*-sampleStrength);
	}   

	fragColor = color/float(samples);
}
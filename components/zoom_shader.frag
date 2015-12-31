layout(location = 0) out vec4 fragColor;
uniform vec2 center;
uniform int samples;
uniform float strength;

void main(void)
{

	vec2 res = uTD2DInfos[0].res.zw;
	vec2 pos = center * res;
	vec2 dir = (gl_FragCoord.xy-pos)/res;
	
	float strengthMult = texture(sTD2DInputs[1], vUV.st).r;
	strengthMult=1;
	float actualStrength = strength * strengthMult;

	vec4 color = vec4(0.0,0.0,0.0,0.0);
	   
	for (int i = 0; i < samples; i += 2) //operating at 2 samples for better performance
	{
		color += texture(sTD2DInputs[0],vUV.st+float(i)/float(samples)*dir*-actualStrength);
		color += texture(sTD2DInputs[0],vUV.st+float(i+1)/float(samples)*dir*-actualStrength);
	}   

	fragColor = color/float(samples);
}
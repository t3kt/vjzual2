uniform float numtaps;
uniform samplerBuffer active_length_alpha;
uniform samplerBuffer filter_hue_sat_val_on;

#define ACTIVE(ala) ala.x
#define LENGTH(ala) ala.y
#define ALPHA(ala) ala.z

#define FILTERHUE(f) f.x
#define FILTERSAT(f) f.y
#define FILTERVAL(f) f.z
#define FILTERALPHA(f) f.a

vec4 applyFilter(vec4 color, int i) {
	vec4 filterPars = texelFetchBuffer(filter_hue_sat_val_on, i);
	vec4 filterColor = vec4(TDHSVToRGB(filterPars.xyz), 1);
	vec4 filtered = color * filterColor;
	return mix(color, filtered, FILTERALPHA(filterPars));
}

vec4 getTap(int i)
{
	vec4 ala = texelFetchBuffer(active_length_alpha, i);
	if (ACTIVE(ala) < 0.5) {
		return vec4(0);
	}
	// The center of the first slice is not located at 0,
	// but rather halfway between 0 (the start of the first slice)
    // and 1.0 / depth (the end of the first slice)
    float w = uTD3DInfos[0].depth.x * 0.5;
     
    // now add the offset
	w += uTD3DInfos[0].depth.z + LENGTH(ala);
	vec3 uvw = vec3(vUV.st, w);
	vec4 color = texture(sTD3DInputs[0], uvw);
	color = applyFilter(color, i);
	color.rgb *= color.a;
	return color;
}

out vec4 fragColor;
void main()
{
	// vec4 color = texture(sTD2DInputs[0], vUV.st);
	vec4 color = vec4(0.0);
	color += getTap(0);
	color += getTap(1);
	color += getTap(2);
	color += getTap(3);
	color += getTap(4);
	color += getTap(5);
	color += getTap(6);
	color += getTap(7);
	//int n = int(numtaps);
	//for (int i = 0; i < n; i++)
	//{
	//	color += getTap(i);
	//}
	
	fragColor = color;
}
	
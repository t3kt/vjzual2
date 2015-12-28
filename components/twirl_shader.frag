/*
 *
 * Adopted from:
 * Andrew Benson - andrewb@cycling74.com
 * Copyright 2005 - Cycling '74
 *
 * GLSL vertex program for doing a standard vertex transform
 * with texture coordinates, also passing the texture dimensions to the fragment shader.
 *
 */
 
uniform float twirl;
uniform float size;
uniform vec2 center;

layout(location = 0) out vec4 fragColor;
void main()
{

	vec2 res = uTD2DInfos[0].res.zw;
	vec2 centerS = center * res/2;
	float sizeS = size * res.x/2;
	vec2 normCoord = vec2(2.0) * vUV.st - vec2(1.0);
	normCoord *= res/2;
	normCoord += centerS;

	float r = length(normCoord);
	float phi = atan(normCoord.y, normCoord.x);

	//vec2 r = vec2(length(normCoord)*res.x/res.y,length(normCoord));

	phi = phi + (1.0 - smoothstep(-sizeS, sizeS, r)) * twirl;

	normCoord.x = r * cos(phi);
	normCoord.y = r * sin(phi);

	normCoord -= centerS;
	normCoord /= res/2;
	vec2 texCoord = (normCoord / 2.0 + 0.5);

	fragColor = texture(sTD2DInputs[0],texCoord);
}
// https://www.shadertoy.com/view/4dfGWr
// Kaleidoscope tre - bendy
// by mfagerlund in 2013-Apr-24

layout (location = 0) out vec4 fragColor;
uniform float iGlobalTime;
uniform int numPoints =4;
uniform bool showFolds = false;
uniform bool outputUV = false;
uniform float uvWeight = 1.0;
uniform vec2 center = vec2(0.5, 0.5);

float rand( vec2 n ) {
	return fract(sin(dot(n.xy, vec2(12.9898, 78.233)))* 43758.5453);
}

struct Ray
{
	vec2 point;
	vec2 direction;
};

float noise(vec2 n) {
	const vec2 d = vec2(0.0, 1.0);
	vec2 b = floor(n), f = smoothstep(vec2(0.0), vec2(1.0), fract(n));
	return mix(mix(rand(b), rand(b + d.yx), f.x), mix(rand(b + d.xy), rand(b + d.yy), f.x), f.y);
}

vec2 noise2(vec2 n)
{
	return vec2(noise(vec2(n.x+0.2, n.y-0.6)), noise(vec2(n.y+3., n.x-4.)));
}

Ray GetRay(vec2 pos, int id)
{
	float i = float(id);
	vec2 position;
	
	if(id == 0)
	{
		position = vec2(1.0,0.5);
	} else
	{
		position = noise2(pos+vec2(i*6.12+iGlobalTime*0.1, i*4.43+iGlobalTime*0.1));
	}	
	return Ray(
		position,
		normalize(noise2(vec2(i*7.+iGlobalTime*0.05, i*6.))*2.0-1.0));	
}

void main()
{
	vec2 res = uTD2DInfos[0].res.zw;

	vec2 uv = gl_FragCoord.xy / min(res.x,res.y);
	vec2 curPos = uv + center;
	
	for(int i=0;i<numPoints;i++)
	{
		Ray ray=GetRay(curPos, i);	
			
		if(length(ray.point-curPos)<0.01 && showFolds)
		{
			fragColor.rgb = vec3(1,1,1);
			return;
		}
		else if (length(curPos-(ray.point+ray.direction*0.1))<0.01 && showFolds)
		{
			fragColor.rgb = vec3(1,0,0);
			return;
		}
		else
		{
			float offset=dot(curPos-ray.point, ray.direction);
			if(abs(offset)<0.001 && showFolds)
			{
				fragColor.rgb = vec3(0,0,1);
				return;
			}
			if(offset<0.)
			{
				curPos -= ray.direction*offset*2.0;
			}									
		}
	}

	curPos -= center;
	curPos = mix(vUV.xy, curPos, uvWeight);
	
	if (outputUV) {
		fragColor.rgb = vec3(curPos, 0);
	} else {
		fragColor.rgb = texture( sTD2DInputs[0], curPos ).xyz;
	}
}

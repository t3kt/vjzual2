uniform int[4] tapActiveA;
uniform vec4 tapLengthA;
uniform vec4 tapAlphaA;
uniform int[4] tapActiveB;
uniform vec4 tapLengthB;
uniform vec4 tapAlphaB;
uniform int stepCompMode;

#define COMP_ADD 0
#define COMP_ATOP 1
#define COMP_AVERAGE 2
#define COMP_DIFFERENCE 3
#define COMP_INSIDE 4
#define COMP_MAXIMUM 5
#define COMP_MINIMUM 6
#define COMP_MULTIPLY 7
#define COMP_OUTSIDE 8
#define COMP_OVER 9
#define COMP_SCREEN 10
#define COMP_SUBTRACT 11
#define COMP_UNDER 12

#define W_OFFSET uTD3DInfos[0].depth.z

vec4 getTap(float length, float alpha) {
	return texture(sTD3DInputs[0], vec3(vUV.st, length + W_OFFSET));
}

struct TapResults {
    vec4[8] colors;
    int count;
};

TapResults getTaps() {
    vec4[8] colors;
    int count;

    for (int i = 0; i < 4; i++) {
        if (tapActiveA[i] > 0) {
            colors[count] = getTap(tapLengthA[i], tapAlphaA[i]);
            count++;
        }
    }
    for (int i = 0; i < 4; i++) {
        if (tapActiveB[i] > 0) {
            colors[count] = getTap(tapLengthB[i], tapAlphaB[i]);
            count++;
        }
    }
    return TapResults(colors, count);
}

vec4 compositeTaps_add(vec4[8] colors, int count) {
    vec4 color = vec4(0.0);
    for (int i = 0; i < count; i++) {
        color = color + colors[i];
    }
    return color;
}

vec4 compositeTaps_atop(vec4[8] colors, int count) {
    vec4 color = vec4(0.0, 0.0, 0.0, 1.0);
    for (int i = 0; i < count; i++) {
        color = (color.rgba * colors[i].a) + (colors[i].rgba * (1.0 - color.a));
    }
    return color;
}

vec4 compositeTaps_difference(vec4[8] colors, int count) {
    vec4 color = vec4(0.0, 0.0, 0.0, 1.0);
    for (int i = 0; i < count; i++) {
        color.rgb = abs(color.rgb - colors[i].rgb);
    }
    return color;
}

vec4 compositeTaps_inside(vec4[8] colors, int count) {
    vec4 color = vec4(0.0, 0.0, 0.0, 1.0);
    for (int i = 0; i < count; i++) {
        color = color * clamp(colors[i], 0.0, 1.0);
    }
    return color;
}

vec4 compositeTaps_maximum(vec4[8] colors, int count) {
    vec4 color = vec4(0.0);
    for (int i = 0; i < count; i++) {
        color = max(color, colors[i]);
    }
    return color;
}

vec4 compositeTaps_minimum(vec4[8] colors, int count) {
    vec4 color = vec4(1.0);
    for (int i = 0; i < count; i++) {
        color = min(color, colors[i]);
    }
    return color;
}

vec4 compositeTaps_multiply(vec4[8] colors, int count) {
    vec4 color = vec4(1.0);
    for (int i = 0; i < count; i++) {
        color = color * colors[i];
    }
    return color;
}

vec4 compositeTaps_outside(vec4[8] colors, int count) {
    vec4 color = vec4(0.0, 0.0, 0.0, 1.0);
    for (int i = 0; i < count; i++) {
        color = color * (1.0 - colors[i].a);
    }
    return color;
}

vec4 compositeTaps_over(vec4[8] colors, int count) {
    vec4 color = vec4(0.0, 0.0, 0.0, 0.0);
    for (int i = 0; i < count; i++) {
        color = (colors[i] * (1.0 - color.a)) + color;
    }
    return color;
}

vec4 compositeTaps_screen(vec4[8] colors, int count) {
    vec4 color = vec4(0.0);
    for (int i = 0; i < count; i++) {
        color = 1.0 - ((1.0 - color) * (1.0 - colors[i]));
    }
    return color;
}

vec4 compositeTaps_subtract(vec4[8] colors, int count) {
    vec4 color = vec4(1.0);
    for (int i = 0; i < count; i++) {
        color = color - colors[i];
    }
    return color;
}

vec4 compositeTaps_under(vec4[8] colors, int count) {
    vec4 color = vec4(1.0);
    for (int i = 0; i < count; i++) {
        color = (color * (1.0 - colors[i].a)) + colors[i];
    }
    return color;
}

vec4 compositeTaps(vec4[8] colors, int count) {
	vec4 color = vec4(0.0);
	if (stepCompMode == COMP_ADD) {
	    return compositeTaps_add(colors, count);
	}
	if (stepCompMode == COMP_ATOP) {
	    return compositeTaps_atop(colors, count);
	}
	if (stepCompMode == COMP_AVERAGE) {
	    return compositeTaps_add(colors, count) / count;
	}
	if (stepCompMode == COMP_DIFFERENCE) {
	    return compositeTaps_difference(colors, count);
	}
	if (stepCompMode == COMP_INSIDE) {
	    return compositeTaps_inside(colors, count);
	}
	if (stepCompMode == COMP_MAXIMUM) {
	    return compositeTaps_maximum(colors, count);
	}
	if (stepCompMode == COMP_MINIMUM) {
	    return compositeTaps_minimum(colors, count);
	}
	if (stepCompMode == COMP_MULTIPLY) {
	    return compositeTaps_multiply(colors, count);
	}
	if (stepCompMode == COMP_OUTSIDE) {
	    return compositeTaps_outside(colors, count);
	}
	if (stepCompMode == COMP_OVER) {
	    return compositeTaps_over(colors, count);
	}
	if (stepCompMode == COMP_SCREEN) {
	    return compositeTaps_screen(colors, count);
	}
	if (stepCompMode == COMP_SUBTRACT) {
	    return compositeTaps_subtract(colors, count);
	}
	if (stepCompMode == COMP_UNDER) {
	    return compositeTaps_under(colors, count);
	}
    return color;
}

out vec4 fragColor;
void main()
{
    TapResults taps = getTaps();
	vec4 color = vec4(0.0);
	if (tapActiveA[0] > 0.0) {
		color += getTap(tapLengthA.x, tapAlphaA.x);
	}
	if (tapActiveA[1] > 0.0) {
		color += getTap(tapLengthA.y, tapAlphaA.y);
	}
	if (tapActiveA[2] > 0.0) {
		color += getTap(tapLengthA.z, tapAlphaA.z);
	}
	if (tapActiveA[3] > 0.0) {
		color += getTap(tapLengthA.w, tapAlphaA.w);
	}
	fragColor = color;
}
	
var raw = d; // 'd' being the defined value in the <script> tag used to "generate" the puzzle (it's just compressed data)

//// process raw data
column_count = raw[1][0] % raw[1][3] + raw[1][1] % raw[1][3] - raw[1][2] % raw[1][3];
row_count = raw[2][0] % raw[2][3] + raw[2][1] % raw[2][3] - raw[2][2] % raw[2][3];
color_count = raw[3][0] % raw[3][3] + raw[3][1] % raw[3][3] - raw[3][2] % raw[3][3];

for (var i = 5; i < color_count + 5; i++) {
    colors[i - 5] = (raw[i][0] - raw[4][1] + 256).toString(16).substring(1) + ((raw[i][1] - raw[4][0] + 256 << 8) + (raw[i][2] - raw[4][3])).toString(16).substring(1);
}
////

//// init
for (var i = 0; i < column_count; i++) {
    result_columns[i] = [];
    for (var j = 0; j < row_count; j++) {
        result_columns[i][j] = 0;
    }
}
////

//// get grid values ([columns][rows])
var a = color_count + 5;
var b = raw[a][0] % raw[a][3] * (raw[a][0] % raw[a][3]) + raw[a][1] % raw[a][3] * 2 + raw[a][2] % raw[a][3];
var c = a + 1;
for (i = a + 2; i <= a + 1 + b; i++) {
    for (j = raw[i][0] - raw[c][0] - 1; j < raw[i][0] - raw[c][0] + raw[i][1] - raw[c][1] - 1; j++) {
        result_columns[j][raw[i][3] - raw[c][3] - 1] = raw[i][2] - raw[c][2];
    }
}
////

// the results I need are : 'colors' and 'results_columns', with them, I can build the nonograms (even colored ones)
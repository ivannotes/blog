var columns = {
  1: null,
  2: null,
  3: null,
  4: null
};
var orig_heights = {
  1: 0,
  2: 0,
  3: 0,
  4: 0,
  total: 0
};

function showColumns() {
  // we only care about columns heights when we're in this range
  var width = $(window).width();
  if (width < 750 || width >= 1600) {
    columns[1].css({minHeight: orig_heights[1] + 'px'});
    columns[4].css({minHeight: orig_heights[4] + 'px'});
    return;
  }

  var min = Math.max(columns[2].height(), columns[3].height());
  //console.log('Min: ' + min);

  var victim = columns[4];
  if (victim.css('display') == 'none') {
    victim = columns[1];
    //console.log('Col1 is mah victim');
  } else {
    min -= columns[1].height();
  }

  if (orig_heights.total < min) {
    //console.log('Setting victims height to ' + (min));
    victim.css({minHeight: min + 'px'});
  }
}

$(document).ready(function () {
  columns[1] = $('.col1');
  columns[2] = $('.col2');
  columns[3] = $('.col3');
  columns[4] = $('.col4');

  // get the original column heights
  for (key in columns) {
    col = columns[key];
    orig_heights[key] = col.height();
  }
  orig_heights.total = columns[1].height() + columns[4].height();
  orig_heights.minimum = Math.min(columns[2].height(), columns[3].height());

  //console.log('Total: ' + orig_heights.total);

  showColumns();
  $(window).resize(showColumns);
});

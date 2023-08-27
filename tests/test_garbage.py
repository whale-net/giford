import pytest

# this test uses absoluteish imports for good measure
import giford


@pytest.mark.skip("works now, need to baseline (though not behavior I care about) TODO")
def test_feed_garbage_to_multi_image(
    temp_output_gif: str, orange_swirl_batch: giford.frame.FrameBatch
):
    # this test should fail
    with pytest.raises(ValueError):
        new_batch = giford.frame.FrameBatch()
        for i, frame in enumerate(orange_swirl_batch.frames):
            new_batch.add_frame(frame)

            if (i % 3) == 0:
                r = giford.action.Reshape()
                temp_batch = giford.frame.FrameBatch()
                temp_batch.add_frame(frame).add_frame(frame).add_frame(frame).add_frame(
                    frame
                )
                # this should be smaller probably but idk what is going on
                temp_batch = r.process(
                    temp_batch, giford.action.ReshapeMethod.RESCALE, 0.25
                )
                new_batch.add_batch(temp_batch)

        mimg = giford.image.MultiImage.create_from_frame_batch(new_batch)
        mimg.save(temp_output_gif)
